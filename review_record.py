import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from pymysql import *
from tkcalendar import *

from Print import PrintClass
from details import *
class Review_Record_class:
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

        self.head=Label(self.window,text="Employee Review Record",background=mycolor1,foreground=mycolor4,font=myfont2,relief="raised",borderwidth=10)
        #----------------------Table------------------------
        self.mytable = Treeview(self.window, columns=["c1", "c2", "c3", "c4", "c5"])
        self.mytable.heading("c2", text="Employee Id")
        self.mytable.heading("c1", text="Name")
        self.mytable.heading("c3", text="Date")
        self.mytable.heading("c4", text="Rating")
        self.mytable.heading("c5", text="Comment")
        self.mytable["show"] = "headings"
        self.mytable.column("c1", width=150, anchor="center")
        self.mytable.column("c2", width=150, anchor="center")
        self.mytable.column("c3", width=150, anchor="center")
        self.mytable.column("c4", width=150, anchor="center")
        self.mytable.column("c5", width=600, anchor="center")
        #-------------------------Buttons-------------------------
        self.b1 = Button(self.window, text="Print", background=mycolor3, foreground=mycolor1, font=myfont1,
                         command=self.getprintout)

        #-----------------------Layout---------------------
        x1,y1=70,80
        xdiff=150
        ydiff=50
        self.head.place(x=0,y=0,width=s_w1,height=70)
        y1 += ydiff
        self.mytable.place(x=x1,y=y1,height=420)
        y1 = y1 + 450
        self.b1.place(x=x1 + 520, y=y1, height=40, width=200)

        #--------------------Calls--------------------
        self.Database_connect()
        self.Get_All_Data()
        self.window.mainloop()

    def Database_connect(self):
        try:
            self.conn=connect(host=myhost,user=myuser,password=mypass,database=mydb)
            self.curr=self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e),parent=self.window)
    def Get_All_Data(self):
        try:
            qry="select * from review "
            rowcount=self.curr.execute(qry)
            data=self.curr.fetchall()
            self.pdata=[]
            if data:
                for row in data:
                    myrow=[row[0],row[1],row[2],row[3]]
                    self.pdata.append(myrow)
                    self.mytable.insert("",END,values=row)
            else:
                messagebox.showwarning("Empty","No record found",parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query "+str(e),parent=self.window)
    def getprintout(self):
        pdf = PrintClass()
        #employee_id	name		designation	department	dob	phone_number	email	address	gender	salary

        headings = ['Employee Id', 'Name', 'Review Date', 'Rating']


        pdf.content(f"Employee Review", headings, self.pdata)

        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')


if __name__=="__main__":
    temp=Tk()
    Review_Record_class(temp)
    temp.mainloop()











