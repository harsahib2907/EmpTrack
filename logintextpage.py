from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
from PIL import Image,ImageTk
from details import *
import pymysql
from tkcalendar import *
class LoginTextclass:
    def __init__(self):
        self.window = Tk()
        #---------- settings ----------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        s_w1 = w // 2
        s_h1 = h // 2
        s_x1 = w // 4
        s_y1 = h // 4
        self.window.geometry("%dx%d+%d+%d" % (s_w1, s_h1, s_x1, s_y1))  # w,h,x,y,
        self.window.minsize(s_w1,s_h1)
        self.window.maxsize(s_w1,s_h1)

        #--------------------------------------------------
        self.window.config(background=mycolor1)

        self.hdlbl= Label(self.window,text="Welcome to "+app_name,background=mycolor3,foreground=mycolor1,font=headingfont,relief='groove',borderwidth=5)

        self.L1 = Label(self.window,text="Username",background=mycolor1,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window,text="Password",background=mycolor1,foreground=mycolor4,font=myfont1)

        self.e1 = Entry(self.window,font=myfont1)
        self.e2 =Entry(self.window,font=myfont1,show='*')



        # ---------------- Buttons ------------------------
        self.b1 = Button(self.window,text="Login",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.checkData)
        self.b2 = Button(self.window,text="Reset",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.clearpage)
        self.b3 = Button(self.window,text="Try another way",background=mycolor3,foreground=mycolor1,font=myfont1,command=self.openanotherpage)

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
        self.b2.place(x=x1,y=y1,width=150,height=40)
        self.b1.place(x=x1+xdiff+50,y=y1,width=150,height=40)
        y1+=ydiff
        self.b3.place(x=x1,y=y1,width=300+50,height=40)

        # --------- call required functions --------
        self.databaseConnection()
        self.clearpage()
        self.window.mainloop()


    def openanotherpage(self):
        self.window.destroy()
        from faceloginpage import FaceLoginClass
        FaceLoginClass()


    def databaseConnection(self):
        try:
            self.conn = pymysql.connect(host=myhost, user=myuser, password=mypass, db=mydb)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e),parent=self.window)



    def clearpage(self):
        self.e1.delete(0,END)
        self.e2.delete(0,END)

    def checkData(self):
        try:
            qry = "select * from user where user_name=%s and password=%s"
            rowcount = self.curr.execute(qry , (self.e1.get(),self.e2.get()))
            data = self.curr.fetchone()
            if data:
                un = data[0]
                ut = data[2]
                self.window.destroy()
                from homepage import Homeclass
                Homeclass(un,ut)

            else:
                messagebox.showwarning("Empty","Wrong username or password",parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),parent=self.window)



# ----------for  testing ----------
if __name__ == '__main__':
    LoginTextclass()