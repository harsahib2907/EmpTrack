from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview

from PIL import Image,ImageTk
from dateutil.utils import today
from pymysql import *
import tkcalendar as calc
from datetime import *

from details import *
class Review_class:
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

        self.head=Label(self.window,text="Employee Review",background=mycolor1,foreground=mycolor4,font=myfont2,relief="raised",borderwidth=10)
        #--------------------Labels----------------------
        self.L1=Label(self.window,text="Employee Id",background=mycolor2,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window, text="Name", background=mycolor2, foreground=mycolor4, font=myfont1)
        self.L3 = Label(self.window, text="Date", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L4 = Label(self.window, text="Rating", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L5 = Label(self.window, text="Comment", background=mycolor2, foreground=mycolor4,font=myfont1)


        #----------------------Entries---------------------------
        self.e1=Entry(self.window, background=mycolor3,foreground=mycolor4, font=myfont1)
        self.e1.bind("<KeyRelease>",lambda e: self.getName())
        self.e2=Entry(self.window, background=mycolor3,foreground=mycolor4, font=myfont1)
        self.e3 = calc.DateEntry(self.window, borderwidth=2, date_pattern='y-mm-dd', background=mycolor3,
                            foreground=mycolor4, font=myfont1)
        self.e3.set_date(date.today())
        self.e4=Entry(self.window, background=mycolor3,foreground=mycolor4, font=myfont1)
        self.e5 = Text(self.window, background=mycolor3, foreground=mycolor4, font=myfont1,width=20,height=3)
        #------------------Buttons-------------------
        self.b1=Button(self.window,text="Mark \nReview",background=mycolor3,foreground=mycolor2,font=myfont1,command=self.SaveData)
        self.b2 = Button(self.window, text="Update", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.UpdateData)
        self.b3 = Button(self.window, text="Delete", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.DeleteData)
        self.b4 = Button(self.window, text="Reset", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.Clearpage)
        self.b5 = Button(self.window, text="Fetch", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.Fetchdata)
        self.b6 = Button(self.window, text="Search", background=mycolor3, foreground=mycolor2, font=myfont1,
                         command=self.Search_Data)
        #----------------------Table------------------------
        self.mytable=Treeview(self.window,columns=["c1","c2","c3","c4","c5"])
        self.mytable.heading("c2",text="Employee Id")
        self.mytable.heading("c1",text="Name")
        self.mytable.heading("c3",text="Date")
        self.mytable.heading("c4", text="Rating")
        self.mytable.heading("c5", text="Comment")
        self.mytable["show"]="headings"
        self.mytable.column("c1", width=100,anchor="center")
        self.mytable.column("c2", width=100, anchor="center")
        self.mytable.column("c3", width=100, anchor="center")
        self.mytable.column("c4", width=100, anchor="center")
        self.mytable.column("c5", width=400, anchor="center")
        self.mytable.bind("<ButtonRelease-1>",lambda  e : self.Get_Selected_Row())

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
        y1 += ydiff
        self.L3.place(x=x1, y=y1)
        self.e3.place(x=x1 + xdiff, y=y1)
        self.b6.place(x=x1 + 2.7 * xdiff, y=y1, width=100, height=30)
        y1 += ydiff
        self.L4.place(x=x1, y=y1)
        self.e4.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L5.place(x=x1, y=y1)
        self.e5.place(x=x1 + xdiff, y=y1)
        y1+=ydiff+ydiff
        self.b1.place(x=x1, y=y1,width=100,height=40)
        self.b2.place(x=x1+xdiff+10, y=y1, width=100, height=40)
        y1 += ydiff
        self.b3.place(x=x1, y=y1+10, width=100, height=40)
        self.b4.place(x=x1 + xdiff + 10, y=y1+10, width=100, height=40)
        #--------------------Calls--------------------
        self.Database_connect()
        self.getAllEmpId()
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
            qry="insert into review values(%s,%s,%s,%s,%s)"
            rowcount=self.curr.execute(qry , (self.e1.get().strip(),self.e2.get(),self.e3.get(),self.e4.get(),self.e5.get("0.0",END)))
            self.conn.commit()
            if rowcount==1:
                messagebox.showinfo("Success","Data saved successfully",parent=self.window)
                self.Clearpage()
                self.Search_Data()
            else:
                messagebox.showwarning("Failure","Data not saved",parent=self.window)
        except Exception as e :
            messagebox.showerror("Query Error","Error while executing query",parent=self.window)
    def UpdateData(self):
        #user_name	name	date	status
        if self.Validation()==False:
            return
        try:
            qry="update review set name=%s,date=%s,rating=%s,comments=%s where emp_id=%s"
            rowcount=self.curr.execute(qry , (self.e2.get(),self.e3.get(),self.e4.get(),self.e5.get("0.0",END),self.e1.get().strip()))
            self.conn.commit()
            if rowcount==1:
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
                qry="delete from review where emp_id=%s"
                rowcount=self.curr.execute(qry , (self.e1.get()))
                self.conn.commit()
                if rowcount==1:
                    messagebox.showinfo("Success","Data deleted successfully",parent=self.window)
                    self.Clearpage()
                else:
                    messagebox.showwarning("Failure","Data not deleted",parent=self.window)
            except Exception as e :
                messagebox.showerror("Query Error","Error while executing query",parent=self.window)

    def Clearpage(self):
        self.e1.delete(0,END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
        self.e4.delete(0,END)
        self.e5.delete("0.0",END)
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
            qry = "select * from  review  where emp_id=%s"
            rowcount = self.curr.execute(qry,empid)
            data=self.curr.fetchone()
            self.Clearpage()
            if data:
                self.e1.insert(0,data[0])
                self.e2.insert(0,data[1])
                self.e3.insert(0,data[2])
                self.e4.insert(0,data[3])
                self.e5.insert("0.0",data[4])

            else:
                messagebox.showwarning("Empty", "No Record found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error", "Error while executing query"+str(e), parent=self.window)
    def Search_Data(self):
            try:
                qry="select * from review where date like %s"
                rowcount=self.curr.execute(qry , (self.e3.get()+"%"))
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
        if len(self.e3.get())<1 :
            messagebox.showwarning("Validation", "Enter Date", parent=self.window)
            return False
        elif len(self.e1.get())<1 or int(self.e1.get()) not in self.empid_list:
            messagebox.showwarning("Validation", "Enter Proper Employee Id", parent=self.window)
            return False
        elif 5<float(self.e4.get())<0:
            messagebox.showwarning("Validation", "Enter proper rating", parent=self.window)
            return False
        return True
    def getName(self):
        try:
            qry = "select * from empolyees where employee_id=%s"
            rowcount = self.curr.execute(qry,(self.e1.get()))
            data = self.curr.fetchone()
            # print("data = ",data)
            if data:
                self.e2.delete(0,END)
                self.e2.insert(0,data[1])

        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),parent=self.window)
    def getAllEmpId(self):
        try:
            qry = "select * from empolyees"
            rowcount = self.curr.execute(qry)
            data = self.curr.fetchall()
            self.empid_list=[]
            if data:
                for row in data:
                    self.empid_list.append(row[0])
        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),parent=self.window)
if __name__=="__main__":
    temp=Tk()
    Review_class(temp)
    temp.mainloop()











