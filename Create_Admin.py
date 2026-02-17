from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview

import face_recognition
from PIL import Image,ImageTk
from details import *
import pymysql
from tkcalendar import DateEntry
class CreateAdminClass:
    defaultname = "DefaultImage.jpg"
    def __init__(self):
        self.window = Tk()
        #---------- settings ----------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        s_w1 = w // 2
        s_h1 = h // 2+200
        s_x1 = w // 4
        s_y1 = h // 4-100
        self.window.geometry("%dx%d+%d+%d" % (s_w1, s_h1, s_x1, s_y1))  # w,h,x,y,
        self.window.minsize(s_w1,s_h1)
        self.window.maxsize(s_w1,s_h1)
        #--------------------------------------------------
        self.window.config(background=mycolor1)

        self.hdlbl= Label(self.window,text="Welcome to "+app_name,background=mycolor3,foreground=mycolor1,font=headingfont,relief='groove',borderwidth=5)

        self.L1 = Label(self.window,text="Username",background=mycolor1,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window,text="Password",background=mycolor1,foreground=mycolor4,font=myfont1)
        self.L3 = Label(self.window,text="Usertype",background=mycolor1,foreground=mycolor4,font=myfont1)
        self.L4 = Label(self.window,text="Picture",background=mycolor1 ,foreground=mycolor4,font=myfont1)

        self.e1 = Entry(self.window,font=myfont1)
        self.e2 =Entry(self.window,font=myfont1,show='*')
        self.v1 =StringVar()
        self.c1 = Combobox(self.window,values=['Admin','HR'],textvariable=self.v1,font=myfont1,state='disabled')
        self.c1.current(0)

        # ---------------- Buttons ------------------------
        self.b1 = Button(self.window,text="Save",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.saveData)
        self.b4 = Button(self.window,text="Reset",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.clearpage)

        self.b7 = Button(self.window,text="Choose",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.chooseImage)
        self.b8 = Button(self.window,text="Capture",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.openCapturePic)
        self.imglbl = Label(self.window,borderwidth=1,relief='groove')

        # ---------- placements -----------------

        x1,y1 = s_w1//4,80
        xdiff = 150
        ydiff = 50

        self.hdlbl.place(x=0,y=0,height=70,width=s_w1)

        self.L1.place(x=x1,y=y1)
        self.e1.place(x=x1+xdiff,y=y1)
        y1+=ydiff
        self.L2.place(x=x1,y=y1)
        self.e2.place(x=x1+xdiff,y=y1)
        y1+=ydiff
        self.L3.place(x=x1,y=y1)
        self.c1.place(x=x1+xdiff,y=y1)
        y1+=ydiff
        self.L4.place(x=x1,y=y1)
        self.imgsize=150
        self.imglbl.place(x=x1+xdiff,y=y1,width=self.imgsize,height=self.imgsize)
        y1+=10
        self.b7.place(x=x1+xdiff,y=y1+self.imgsize,width=self.imgsize,height=40)

        y1+=self.imgsize
        y1+=ydiff
        self.b8.place(x=x1+xdiff,y=y1,width=self.imgsize,height=40)
        y1+=ydiff
        self.b4.place(x=x1-10,y=y1,width=150,height=40)
        self.b1.place(x=x1+xdiff,y=y1,width=150,height=40)

        # --------- call required functions --------
        self.databaseConnection()
        self.window.bind("<FocusIn>",lambda e : self.show_capture_img())
        self.flag=False
        self.clearpage()
        self.window.mainloop()



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

                self.simg = Image.open("user_images//" + self.actualname).resize((self.imgsize, self.imgsize))
                self.sphoto = ImageTk.PhotoImage(self.simg)
                self.imglbl.config(image=self.sphoto)

    def openCapturePic(self):
        self.flag=True
        from CapturePic import CaptureClass
        CaptureClass(self.window)

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
            # print("path = ",path)
            name = path[-1]
            # print("name = ",name)
            import time
            unique = str(int(time.time()))
            # print("unique = ",unique)
            self.actualname = unique+name
            # print("actual name = ",self.actualname)

            # ------- check face in image -----------
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) != 1:
                messagebox.showwarning("Input Error", "Please Select One Face Image ", parent=self.window)
                self.actualname = self.defaultname

                self.simg = Image.open("User_Img//"+self.actualname).resize( (self.imgsize,self.imgsize))
                self.sphoto = ImageTk.PhotoImage(self.simg)
                self.imglbl.config(image=self.sphoto)

    def databaseConnection(self):
        try:
            self.conn = pymysql.connect(host=myhost, user=myuser, password=mypass, db=mydb)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e),parent=self.window)

    def saveData(self):
        if self.validationcheck()==False:
            return # stop this function now
        try:
            #	rollno	name	phone	gender	dob	address	department	course
            qry = "insert into user values(%s,%s,%s,%s)"
            rowcount = self.curr.execute(qry , (self.e1.get(),self.e2.get(),self.v1.get(),self.actualname))
            self.conn.commit()
            if rowcount==1:
                un = self.e1.get()
                #------------ save image in folder --------------
                if self.actualname!=self.defaultname: # new image is selected
                    self.simg.save("User_Img//"+self.actualname)
                #-------------------------------------------

                messagebox.showinfo("Success","Admin created successfully",parent=self.window)
                self.clearpage()
                self.window.destroy()
                from homepage import Homeclass
                Homeclass(un,"Admin")
            else:
                messagebox.showwarning("Failure","Data not saved successfully",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),parent=self.window)

    def clearpage(self):
        self.e1.delete(0,END)
        self.e2.delete(0,END)
        self.actualname = self.defaultname
        self.simg = Image.open("User_Img//"+self.defaultname).resize( (self.imgsize,self.imgsize))
        self.sphoto = ImageTk.PhotoImage(self.simg)
        self.imglbl.config(image=self.sphoto)

    def validationcheck(self):
        return True


# ----------for  testing ----------
if __name__ == '__main__':
    CreateAdminClass()