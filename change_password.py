from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
from PIL import Image,ImageTk
from pymysql import *
from tkcalendar import *
import cmake



from details import *
class Change_Password_class:
    def __init__(self,pwindow,un):
        self.uname=un
        self.window=Toplevel(pwindow)
        #----------------Settings--------------------
        w=self.window.winfo_screenwidth()
        h=self.window.winfo_screenheight()

        s_w1=w-200
        s_h1=h-180
        self.window.minsize(s_w1,s_h1)
        self.window.geometry("%dx%d+%d+%d"%(s_w1,s_h1,160,100))

        self.window.config(background=mycolor2)

        self.head=Label(self.window,text="Change Password",background=mycolor1,foreground=mycolor4,font=myfont2,relief="raised",borderwidth=10)
        #--------------------Labels----------------------
        self.L1=Label(self.window,text="Current Password",background=mycolor2,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window, text="New Password", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L3 = Label(self.window, text="Confirm Password", background=mycolor2, foreground=mycolor4,font=myfont1)

        #----------------------Entries---------------------------
        self.e1=Entry(self.window,background=mycolor3,foreground=mycolor1,font=myfont1)
        self.e2 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1,show="*")
        self.e3 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1,show="*")


        #------------------Buttons-------------------
        self.b2 = Button(self.window, text="Change", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.UpdateData)
        self.b4 = Button(self.window, text="Reset", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.Clearpage)

        #-----------------------Layout---------------------
        x1,y1=10,80
        xdiff=200
        ydiff=40
        self.head.place(x=0,y=0,width=s_w1,height=70)

        self.L1.place(x=x1,y=y1)
        self.e1.place(x=x1+xdiff,y=y1)
        y1+=ydiff
        self.L2.place(x=x1, y=y1)
        self.e2.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L3.place(x=x1, y=y1)
        self.e3.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.b2.place(x=x1+xdiff, y=y1, width=110, height=40)
        self.b4.place(x=x1 + 2*xdiff , y=y1, width=100, height=40)
        #--------------------Calls--------------------
        self.Database_connect()
        self.Clearpage()
        self.window.mainloop()

    def Database_connect(self):
        try:
            self.conn=connect(host=myhost,user=myuser,password=mypass,database=mydb)
            self.curr=self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e),parent=self.window)

    def UpdateData(self):
        if self.Validation()==False:
            return
        if self.e2.get()!=self.e3.get():
            messagebox.showwarning("Failure","Confirm password carefully",parent=self.window)
            return
        try:
            qry="update user set password=%s where user_name=%s and password=%s"
            rowcount=self.curr.execute(qry , (self.e2.get(),self.uname,self.e1.get()))
            self.conn.commit()
            if rowcount==1:
                messagebox.showinfo("Success","Password Changed successfully ",parent=self.window)
                self.Clearpage()
                self.Search_Data()
            else:
                messagebox.showwarning("Failure","Password not 000000000000000000000000000000000000000000000000000000Changed",parent=self.window)
        except Exception as e :
            messagebox.showerror("Query Error","Error while executing query",parent=self.window)

    def Clearpage(self):
        self.e1.delete(0,END)
        self.e2.delete(0, END)
        self.e3.delete(0,END)
    def Validation(self):
        if len(self.e1.get())<8   :
            messagebox.showwarning("Validation","Enter proper password",parent=self.window)
            return False
        elif len(self.e2.get())<8 or not self.e2.get().isalnum() :
            messagebox.showwarning("Validation","Enter proper Password",parent=self.window)
            return False
        return True




if __name__=="__main__":
    temp=Tk()
    Change_Password_class(temp,"abc")
    temp.mainloop()












