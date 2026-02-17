from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
from PIL import Image,ImageTk
from pymysql import *
from tkcalendar import *
from CapturePic import *
import face_recognition



from details import *
class User_class:
    defaultname = "DefaultImage.jpg"
    def __init__(self,window):
        self.window=Toplevel(window)
        #----------------Settings--------------------
        w=self.window.winfo_screenwidth()
        h=self.window.winfo_screenheight()

        s_w1=w-200
        s_h1=h-180
        self.window.minsize(s_w1,s_h1)
        self.window.geometry("%dx%d+%d+%d"%(s_w1,s_h1,160,100))

        mycolor1 = "#222831"
        mycolor2 = "#31363F"
        mycolor3 = "#76ABAE"
        mycolor4 = "#EEEEEE"
        myfont1=("Lato",14)
        myfont2=("PT Serif",16,"bold")

        self.window.config(background=mycolor2)

        self.head=Label(self.window,text="USER",background=mycolor1,foreground=mycolor4,font=myfont2,relief="raised",borderwidth=10)
        #--------------------Labels----------------------
        self.L1=Label(self.window,text="Username",background=mycolor2,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window, text="Password", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L3 = Label(self.window, text="Usertype", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L4 = Label(self.window, text="Picture", background=mycolor2, foreground=mycolor4,font=myfont1)


        #----------------------Entries---------------------------
        self.e1=Entry(self.window,background=mycolor3,foreground=mycolor1,font=myfont1)
        self.e2 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1,show="*")
        self.v3=StringVar()
        self.c3 = Combobox(self.window,textvariable=self.v3,values=["Admin","HR"] ,background=mycolor3, foreground=mycolor1, font=myfont1,state="readonly")

        #------------------Buttons-------------------
        self.b1=Button(self.window,text="Save",background=mycolor3,foreground=mycolor2,font=myfont2,command=self.SaveData)
        self.b2 = Button(self.window, text="Update", background=mycolor3, foreground=mycolor2, font=myfont2,
                         command=self.UpdateData)
        self.b3 = Button(self.window, text="Delete", background=mycolor3, foreground=mycolor2, font=myfont2,
                         command=self.DeleteData)
        self.b4 = Button(self.window, text="Reset", background=mycolor3, foreground=mycolor2, font=myfont2,
                         command=self.Clearpage)
        self.b5 = Button(self.window, text="Fetch", background=mycolor3, foreground=mycolor2, font=myfont2,
                         command=self.Fetchdata)
        self.b6 = Button(self.window, text="Search", background=mycolor3, foreground=mycolor2, font=myfont2,
                         command=self.Search_Data)
        self.b8 = Button(self.window, text="Show", background=mycolor3, foreground=mycolor2, font=myfont2,
                         command=self.ShowPassword)
        #----------------------Table------------------------
        self.mytable=Treeview(self.window,columns=["c1","c2"])
        self.mytable.heading("c1",text="Username")
        self.mytable.heading("c2",text="Usertype")

        self.mytable["show"]="headings"
        self.mytable.column("c1", width=300,anchor="center")
        self.mytable.column("c2", width=300, anchor="center")
        self.mytable.bind("<ButtonRelease-1>",lambda  e : self.Get_Selected_Row())

        #----------------------Image Capture---------------------------
        self.b7 = Button(self.window, text="Choose", background=mycolor3, foreground=mycolor1, font=myfont1,
                         command=self.chooseImage)
        self.b9 = Button(self.window, text="Capture", background=mycolor3, foreground=mycolor1, font=myfont1,
                         command=self.openCapturePic)
        self.imglbl = Label(self.window, borderwidth=1, relief='groove')
        #-----------------------Layout---------------------
        x1,y1=10,80
        xdiff=150
        ydiff=40
        self.head.place(x=0,y=0,width=s_w1,height=70)

        self.L1.place(x=x1,y=y1)
        self.e1.place(x=x1+xdiff,y=y1)
        self.b5.place(x=x1+2.6*xdiff,y=y1,width=100,height=30)
        self.mytable.place(x=x1 + 3.3*xdiff,y=y1,height=300)
        y1+=ydiff
        self.L2.place(x=x1, y=y1)
        self.e2.place(x=x1 + xdiff, y=y1)
        self.b8.place(x=x1+xdiff*2.6,y=y1,width=100,height=30)
        y1 += ydiff
        self.L3.place(x=x1, y=y1)
        self.c3.place(x=x1 + xdiff, y=y1,width=230)
        self.b6.place(x=x1 + 2.6 * xdiff, y=y1, width=100, height=30)
        y1 += ydiff
        self.L4.place(x=x1, y=y1)
        self.imgsize = 150
        self.imglbl.place(x=x1 + xdiff, y=y1, width=self.imgsize, height=self.imgsize)
        self.b7.place(x=x1 + xdiff, y=y1 + self.imgsize, width=self.imgsize, height=40)
        self.b9.place(x=x1 + xdiff, y=y1 + self.imgsize+50, width=self.imgsize, height=40)
        y1 += ydiff*6
        self.b1.place(x=x1, y=y1,width=100,height=40)
        self.b2.place(x=x1+xdiff+10, y=y1, width=100, height=40)
        y1 += ydiff
        self.b3.place(x=x1, y=y1+10, width=100, height=40)
        self.b4.place(x=x1 + xdiff + 10, y=y1+10, width=100, height=40)
        #--------------------Calls--------------------
        self.Database_connect()
        self.window.bind("<FocusIn>", lambda e: self.show_capture_img())
        self.flag = False
        self.Clearpage()
        self.window.mainloop()

    def Database_connect(self):
        try:
            self.conn=connect(host=myhost,user=myuser,password=mypass,database=mydb)
            self.curr=self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e),parent=self.window)
    def SaveData(self):
        if self.Validation()==False:
            return
        #employee_id	name		designation	department	dob	phone_number	email	address	gender	salary
        try:
            qry="insert into user values(%s,%s,%s,%s)"
            rowcount=self.curr.execute(qry , (self.e1.get(),self.e2.get(),self.v3.get(),self.actualname))
            self.conn.commit()
            if rowcount==1:
                # ------------ save image in folder --------------
                if self.actualname != self.defaultname:  # new image is selected
                    self.simg.save("User_Img//" + self.actualname)
                # -------------------------------------------
                messagebox.showinfo("Success","Data saved successfully",parent=self.window)
                self.Clearpage()
                self.Search_Data()
            else:
                messagebox.showwarning("Failure","Data not saved",parent=self.window)
        except Exception as e :
            messagebox.showerror("Query Error","Error while executing query",parent=self.window)
    def UpdateData(self):
        if self.Validation()==False:
            return
        try:
            qry="update user set password=%s,user_type=%s,user_pic=%s where user_name=%s"
            rowcount=self.curr.execute(qry , (self.e2.get(),self.v3.get(),self.actualname,self.e1.get()))
            self.conn.commit()
            if rowcount==1:
                # ------------ update image in folder --------------
                if self.actualname != self.oldname:  # new image is selected
                    self.simg.save("User_Img//" + self.actualname)
                    if self.oldname != self.defaultname:  # some image was given in past
                        import os
                        os.remove("User_Img//" + self.oldname)

                # -------------------------------------------
                messagebox.showinfo("Success","Data updated successfully",parent=self.window)
                self.Clearpage()
                self.Search_Data()
            else:
                messagebox.showwarning("Failure","Data not updated",parent=self.window)
        except Exception as e :
            messagebox.showerror("Query Error","Error while executing query",parent=self.window)
    def DeleteData(self):
        ans=messagebox.askquestion("Confirmation","Are you sure to delete ? ",parent=self.window)
        if ans=="yes":
            try:
                qry="delete from user where user_name=%s"
                rowcount=self.curr.execute(qry , (self.e1.get()))
                self.conn.commit()
                if rowcount==1:
                    # ------------ delete image from folder --------------
                    if self.oldname != self.defaultname:  # some image was given in past
                        import os
                        os.remove("User_Img//" + self.oldname)
                    # -------------------------------------------
                    messagebox.showinfo("Success","Data deleted successfully",parent=self.window)
                    self.Clearpage()
                else:
                    messagebox.showwarning("Failure","Data not deleted",parent=self.window)
            except Exception as e :
                messagebox.showerror("Query Error","Error while executing query",parent=self.window)

    def Clearpage(self):
        self.e1.delete(0,END)
        self.e2.delete(0, END)
        self.v3.set("")
        self.actualname = self.defaultname

        self.simg = Image.open("User_Img//" + self.defaultname).resize((self.imgsize, self.imgsize))
        self.sphoto = ImageTk.PhotoImage(self.simg)
        self.imglbl.config(image=self.sphoto)
        self.Search_Data()
    def Get_Selected_Row(self):
        id=self.mytable.focus()
        rowdata=self.mytable.item(id)
        rowvalues=rowdata["values"]
        col1=rowvalues[0]
        self.Fetchdata(col1)
    def Fetchdata(self,pkcol=None):
        if pkcol==None:
            empid=self.e1.get()
        else:
            empid=pkcol
        try:
            qry = "select * from  user  where user_name=%s"
            rowcount = self.curr.execute(qry,empid)
            data=self.curr.fetchone()
            self.Clearpage()
            if data:
                self.e1.insert(0,data[0])
                self.e2.insert(0, data[1])
                self.v3.set(data[2])
                self.actualname = data[3]
                self.oldname = data[3]
                self.simg = Image.open("Emp_Images//" + self.actualname).resize((self.imgsize, self.imgsize))
                self.sphoto = ImageTk.PhotoImage(self.simg)
                self.imglbl.config(image=self.sphoto)
            else:
                messagebox.showwarning("Empty", "No Record found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error", "Error while executing query"+str(e), parent=self.window)
    def Search_Data(self):
            try:
                qry="select * from user where user_type like %s"
                rowcount=self.curr.execute(qry , (self.v3.get()+"%"))
                data=self.curr.fetchall()
                self.mytable.delete(*self.mytable.get_children())
                if data:
                    for row in data:
                        rowdata=[row[0],row[2]]
                        self.mytable.insert("",END,values=rowdata)
                else:
                    messagebox.showwarning("Empty","No Record Found",parent=self.window)
            except Exception as e :
                messagebox.showerror("Query Error","Error while executing query",parent=self.window)
    def Validation(self):
        if len(self.e1.get())<1 :
            messagebox.showwarning("Validation","Enter proper Username",parent=self.window)
            return False
        elif len(self.e2.get())<8 or not self.e2.get().isalnum() :
            messagebox.showwarning("Validation","Enter proper Password",parent=self.window)
            return False
        elif self.v3.get()=="" :
            messagebox.showwarning("Validation","Select User Type",parent=self.window)
            return False
        return True
    def chooseImage(self):
        filename = askopenfilename(filetypes=[ ('All Pictures',"*.jpg;*.png;*.jpeg") , ('PNG Images','*.png') , ('JPG Images','*.jpg')],parent=self.window)
        print("Filename = ",filename)
        if filename!="":
            # resize and set image on label
            self.simg = Image.open(filename).resize( (self.imgsize,self.imgsize))
            self.sphoto = ImageTk.PhotoImage(self.simg)
            self.imglbl.config(image=self.sphoto)

            #create unique name to save
            path = filename.split("/")
            name = path[-1]
            import time
            unique = str(int(time.time()))
            self.actualname = unique+name
    def ShowPassword(self):
        if True :
            self.e2.config(show="")
    def show_capture_img(self):
        if self.flag == True:
            self.flag = False
            #show image on label
            filename = "captured_photo.jpg"

            # resize and set image on label
            self.simg = Image.open(filename).resize((self.imgsize, self.imgsize))
            self.sphoto = ImageTk.PhotoImage(self.simg)
            self.imglbl.config(image=self.sphoto)

            # create unique name to save
            path = filename.split("/")
            # print("path = ",path)
            name = path[-1]
            # print("name = ",name)
            import time
            unique = str(int(time.time()))
            # print("unique = ",unique)
            self.actualname = unique + name
            # print("actual name = ",self.actualname)

            # ------- check face in image -----------
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) != 1:
                messagebox.showwarning("Input Error", "Please Select One Face Image ", parent=self.window)
                self.actualname = self.defaultname

                self.simg = Image.open("User_Img//" + self.actualname).resize((self.imgsize, self.imgsize))
                self.sphoto = ImageTk.PhotoImage(self.simg)
                self.imglbl.config(image=self.sphoto)

    def openCapturePic(self):
        self.flag=True
        from CapturePic import CaptureClass
        CaptureClass(self.window)



if __name__=="__main__":
    temp=Tk()
    User_class(temp)
    temp.mainloop()











