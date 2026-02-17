from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview

from PIL import Image,ImageTk
from pymysql import *
import tkcalendar as  calc

from details import *
class Employee_class:
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
        self.window.config(background=mycolor2)

        self.head=Label(self.window,text="Employee Manager",background=mycolor1,foreground=mycolor4,font=myfont2,relief="raised",borderwidth=10)
        #--------------------Labels----------------------
        self.L1=Label(self.window,text="Employee Id",background=mycolor2,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window, text="Name", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L4 = Label(self.window, text="Department", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L5 = Label(self.window, text="Designation", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L6 = Label(self.window, text="DOB", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L7 = Label(self.window, text="Phone Number", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L8 = Label(self.window, text="E-Mail Address", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L9 = Label(self.window, text="Address", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L10 = Label(self.window, text="Gender", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L11 = Label(self.window, text="Salary", background=mycolor2, foreground=mycolor4,font=myfont1)

        #----------------------Entries---------------------------
        self.e1=Entry(self.window,background=mycolor3,foreground=mycolor1,font=myfont1)
        self.e2 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1)
        self.v5=StringVar()
        self.c5 = Combobox(self.window,textvariable=self.v5, background=mycolor3, foreground=mycolor1, font=myfont1,state="readonly")
        self.v4 = StringVar()
        self.c4 = Combobox(self.window,textvariable=self.v4, background=mycolor3, foreground=mycolor1, font=myfont1,state="readonly")
        self.c4.bind("<<ComboboxSelected>>", lambda e: self.getAllDesignation())
        self.e6 = calc.DateEntry(self.window,borderwidth=2, year=2000,date_pattern='y-mm-dd',background=mycolor3,foreground=mycolor2,font=myfont1)
        self.e7 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1)
        self.e8 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1)
        self.e9 = Text(self.window, background=mycolor3, foreground=mycolor1, font=myfont1,width=20,height=3)
        self.v10=StringVar()
        self.r110=Radiobutton(self.window, text="Male", value="Male",variable=self.v10,background=mycolor2, foreground=mycolor3, font=myfont1)
        self.r210 = Radiobutton(self.window, text="Female", value="Female", variable=self.v10, background=mycolor2,
                                foreground=mycolor3, font=myfont1)
        self.e11= Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1)
        #------------------Buttons-------------------
        self.b1=Button(self.window,text="Save",background=mycolor3,foreground=mycolor2,font=myfont1,command=self.SaveData)
        self.b2 = Button(self.window, text="Update", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.UpdateData)
        self.b3 = Button(self.window, text="Delete", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.DeleteData)
        self.b4 = Button(self.window, text="Reset", background=mycolor3, foreground=mycolor2,  font=myfont1,
                         command=self.Clearpage)
        self.b5 = Button(self.window, text="Fetch", background=mycolor3, foreground=mycolor2,  font=myfont1,
                         command=self.Fetchdata)
        self.b6 = Button(self.window, text="Search", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.Search_Data)
        #----------------------Table------------------------
        self.mytable=Treeview(self.window,columns=["c1","c2","c3","c4","c5","c6","c7","c8","c9","c10"])
        self.mytable.heading("c1",text="Employee Id")
        self.mytable.heading("c2",text="Name")
        self.mytable.heading("c3",text="Designation")
        self.mytable.heading("c4", text="Department")
        self.mytable.heading("c5", text="DOB")
        self.mytable.heading("c6",text="Phone Number")
        self.mytable.heading("c7", text="E-Mail Address")
        self.mytable.heading("c8", text="Address")
        self.mytable.heading("c9", text="Gender")
        self.mytable.heading("c10", text="Salary")
        self.mytable["show"]="headings"
        self.mytable.column("c1", width=80,anchor="center")
        self.mytable.column("c2", width=80, anchor="center")
        self.mytable.column("c3", width=90, anchor="center")
        self.mytable.column("c4", width=80, anchor="center")
        self.mytable.column("c5", width=70, anchor="center")
        self.mytable.column("c6", width=80, anchor="center")
        self.mytable.column("c7", width=110, anchor="center")
        self.mytable.column("c8", width=80, anchor="center")
        self.mytable.column("c9", width=70, anchor="center")
        self.mytable.column("c10",width=70, anchor="center")
        self.mytable.bind("<ButtonRelease-1>",lambda  e : self.Get_Selected_Row())

        #----------------------Image Capture---------------------------
        self.b7 = Button(self.window, text="Choose", background=mycolor3, foreground=mycolor1, font=myfont1,
                         command=self.chooseImage)
        self.imglbl = Label(self.window, borderwidth=1, relief='groove')
        #-----------------------Layout---------------------
        x1,y1=10,80
        xdiff=150
        ydiff=40
        self.head.place(x=0,y=0,width=s_w1,height=70)

        self.L1.place(x=x1,y=y1)
        self.e1.place(x=x1+xdiff,y=y1)
        self.b5.place(x=x1+2.7*xdiff,y=y1,width=100,height=30)
        self.mytable.place(x=x1 + 3.4*xdiff,y=y1,height=300)
        y1+=ydiff
        self.L2.place(x=x1, y=y1)
        self.e2.place(x=x1 + xdiff, y=y1)
        self.b6.place(x=x1 + 2.7 * xdiff, y=y1, width=100, height=30)
        y1 += ydiff
        self.L4.place(x=x1, y=y1)
        self.c4.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L5.place(x=x1, y=y1)
        self.c5.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L6.place(x=x1, y=y1)
        self.e6.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L7.place(x=x1, y=y1)
        self.e7.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L8.place(x=x1, y=y1)
        self.e8.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L9.place(x=x1, y=y1)
        self.e9.place(x=x1 + xdiff, y=y1)
        y1 += ydiff+ydiff
        self.L10.place(x=x1, y=y1)
        self.r110.place(x=x1 + xdiff, y=y1)
        self.r210.place(x=x1 + xdiff+xdiff, y=y1)
        y1 += ydiff
        self.L11.place(x=x1, y=y1)
        self.e11.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.b1.place(x=x1, y=y1,width=100,height=40)
        self.b2.place(x=x1+xdiff+10, y=y1, width=100, height=40)
        y1 += ydiff
        self.b3.place(x=x1, y=y1+10, width=100, height=40)
        self.b4.place(x=x1 + xdiff + 10, y=y1+10, width=100, height=40)

        self.imgsize = 150
        self.imglbl.place(x=x1 + 450, y=y1 - self.imgsize, width=self.imgsize, height=self.imgsize)
        self.b7.place(x=x1 + 450, y=y1, width=self.imgsize, height=40)
        #--------------------Calls--------------------
        self.Database_connect()
        self.getAllDepartment()
        self.Clearpage()
        self.Search_Data()
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
            qry="insert into empolyees values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            rowcount=self.curr.execute(qry , (self.e1.get(),self.e2.get(),self.v4.get(),self.v5.get(),self.e6.get(),self.e7.get(),self.e8.get(),self.e9.get("0.0",END),self.v10.get(),self.e11.get(),self.actualname))
            self.conn.commit()
            if rowcount==1:
                # ------------ save image in folder --------------
                if self.actualname != self.defaultname:  # new image is selected
                    self.simg.save("Emp_Images//" + self.actualname)
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
            qry="update empolyees set name=%s,designation=%s,department=%s,dob=%s,phone_number=%s,email=%s,address=%s,gender=%s,salary=%s,emp_image=%s where employee_id=%s"
            rowcount=self.curr.execute(qry , (self.e2.get(),self.v5.get(),self.v4.get(),self.e6.get(),self.e7.get(),self.e8.get(),self.e9.get("0.0",END),self.v10.get(),self.e11.get(),self.actualname,self.e1.get()))
            self.conn.commit()
            if rowcount==1:
                # ------------ update image in folder --------------
                if self.actualname != self.oldname:  # new image is selected
                    self.simg.save("Emp_Images//" + self.actualname)
                    if self.oldname != self.defaultname:  # some image was given in past
                        import os
                        os.remove("Emp_Images//" + self.oldname)

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
                qry="delete from empolyees where employee_id=%s"
                rowcount=self.curr.execute(qry , (self.e1.get()))
                self.conn.commit()
                if rowcount==1:
                    # ------------ delete image from folder --------------
                    if self.oldname != self.defaultname:  # some image was given in past
                        import os
                        os.remove("Emp_Images//" + self.oldname)
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
        self.v5.set("No Designation")
        self.v4.set(self.c4_msg)
        self.e6.delete(0, END)
        self.e7.delete(0, END)
        self.e8.delete(0, END)
        self.e9.delete("0.0", END)
        self.v10.set(None)
        self.e11.delete(0, END)
        self.actualname = self.defaultname

        self.simg = Image.open("Emp_Images//" + self.defaultname).resize((self.imgsize, self.imgsize))
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
            qry = "select * from  empolyees  where employee_id=%s"
            rowcount = self.curr.execute(qry,empid)
            data=self.curr.fetchone()
            self.Clearpage()
            if data:
                self.e1.insert(0,data[0])
                self.e2.insert(0, data[1])
                self.v5.set(data[2])
                self.v4.set(data[3])
                self.e6.insert(0, data[4])
                self.e7.insert(0, data[5])
                self.e8.insert(0, data[6])
                self.e9.insert("0.0", data[7])
                self.v10.set(data[8])
                self.e11.insert(0,data[9])
                self.actualname = data[10]
                self.oldname = data[10]
                self.simg = Image.open("Emp_Images//" + self.actualname).resize((self.imgsize, self.imgsize))
                self.sphoto = ImageTk.PhotoImage(self.simg)
                self.imglbl.config(image=self.sphoto)
            else:
                messagebox.showwarning("Empty", "No Record found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error", "Error while executing query"+str(e), parent=self.window)
    def Search_Data(self):
            try:
                qry="select * from empolyees where name like %s"
                rowcount=self.curr.execute(qry , (self.e2.get()+"%"))
                data=self.curr.fetchall()
                self.mytable.delete(*self.mytable.get_children())
                if data:
                    for row in data:
                        self.mytable.insert("",END,values=row)
                else:
                    messagebox.showwarning("Empty","No Record Found",parent=self.window)
            except Exception as e :
                messagebox.showerror("Query Error","Error while executing query",parent=self.window)
    def Validation(self):
        if len(self.e1.get())<1 or not self.e1.get().isdigit():
            messagebox.showwarning("Validation","Enter proper Employee Id",parent=self.window)
            return False
        elif len(self.e2.get())<1 :
            messagebox.showwarning("Validation","Enter proper Name",parent=self.window)
            return False
        elif self.v5.get()=="Choose Designation" or self.v5.get()=="No Designation":
            messagebox.showwarning("Validation","Select Designation",parent=self.window)
            return False
        elif self.v4.get() == "Choose Department" or self.v4.get() == "No Department":
            messagebox.showwarning("Validation", "Select Department", parent=self.window)
            return False
        elif len(self.e6.get())<1:
            messagebox.showwarning("Validation", "Enter Proper DOB", parent=self.window)
            return False
        elif len(self.e7.get())!=10 or not self.e7.get().isdigit() :
            messagebox.showwarning("Validation", "Enter Proper Phone Number", parent=self.window)
            return False
        elif len(self.e8.get())<1 or("@" not in self.e8.get() and ".com" not in self.e8.get()) :
            messagebox.showwarning("Validation", "Enter Proper E-Mail Address", parent=self.window)
            return False
        elif len(self.e9.get("0.0",END))<3 :
            messagebox.showwarning("Validation", "Enter Proper Address", parent=self.window)
            return False
        elif not (self.v10.get() == "Male" or self.v10.get() == "Female"):
            messagebox.showwarning("Validation", "Select Gender", parent=self.window)
            return False
        elif len(self.e11.get()) <1 :
            messagebox.showwarning("Validation", "Enter Proper Salary", parent=self.window)
            return False
        return True
    def getAllDepartment(self):
        try:
            qry = "select * from department"
            rowcount = self.curr.execute(qry)
            data = self.curr.fetchall()
            self.deptlist=[]
            if data:
                self.c4_msg = "Choose Department"
                for row in data:
                    self.deptlist.append(row[1])
            else:
                self.c4_msg = "No Department"
            self.c4.config(values=self.deptlist)


        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),parent=self.window)
    def getAllDesignation(self):
        try:
            qry = "select * from designation where department = %s"
            rowcount = self.curr.execute(qry, (self.v4.get()))
            data = self.curr.fetchall()
            self.dessignation_list = []
            if data:
                self.c5.set("Choose Designation")
                for row in data:
                    self.dessignation_list.append(row[1])
            else:
                self.c5.set("No Designation")
            self.c5.config(values=self.dessignation_list)

        except Exception as e:
            messagebox.showerror("Query Error", "Error while executing query : \n" + str(e), parent=self.window)
    def chooseImage(self):
        filename = askopenfilename(filetypes=[ ('All Pictures',"*.jpg;*.png;*.jpeg") , ('PNG Images','*.png') , ('JPG Images','*.jpg')],parent=self.window)
        # print("Filename = ",filename)
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


if __name__=="__main__":
    temp=Tk()
    Employee_class(temp)
    temp.mainloop()











