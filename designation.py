from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from pymysql import *
from tkcalendar import *

from details import *
class Designation_class:
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

        self.head=Label(self.window,text="Designations",background=mycolor1,foreground=mycolor4,font=myfont2,relief="raised",borderwidth=10)
        #--------------------Labels----------------------
        self.L1=Label(self.window,text="Designation Id",background=mycolor2,foreground=mycolor4,font=myfont1)
        self.L2 = Label(self.window, text="Name", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L3 = Label(self.window, text="Abbreviation", background=mycolor2, foreground=mycolor4,font=myfont1)
        self.L4 = Label(self.window, text="Department", background=mycolor2, foreground=mycolor4,font=myfont1)
        #----------------------Entries---------------------------
        self.e1=Entry(self.window,background=mycolor3,foreground=mycolor1,font=myfont1)
        self.e2 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1)
        self.e3 = Entry(self.window, background=mycolor3, foreground=mycolor1, font=myfont1)
        self.v4=StringVar()
        self.c4 = Combobox(self.window,textvariable=self.v4, background=mycolor3, foreground=mycolor1, font=myfont1,state="readonly")
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
        self.mytable=Treeview(self.window,columns=["c1","c2","c3","c4"])
        self.mytable.heading("c1",text="Designation Id")
        self.mytable.heading("c2",text="Name")
        self.mytable.heading("c3",text="Abbreviation")
        self.mytable.heading("c4", text="Department")
        self.mytable["show"]="headings"
        self.mytable.column("c1", width=150,anchor="center")
        self.mytable.column("c2", width=150, anchor="center")
        self.mytable.column("c3", width=150, anchor="center")
        self.mytable.column("c4", width=150, anchor="center")
        self.mytable.bind("<ButtonRelease-1>",lambda  e : self.Get_Selected_Row())

        #-----------------------Layout---------------------
        x1,y1=10,80
        xdiff=150
        ydiff=40
        self.head.place(x=0,y=0,width=s_w1,height=70)

        self.L1.place(x=x1,y=y1)
        self.e1.place(x=x1+xdiff,y=y1)
        self.b5.place(x=x1+2.7*xdiff,y=y1,width=100,height=30)
        self.mytable.place(x=x1 + 3.4*xdiff,y=y1)
        y1+=ydiff
        self.L2.place(x=x1, y=y1)
        self.e2.place(x=x1 + xdiff, y=y1)
        self.b6.place(x=x1 + 2.7* xdiff, y=y1, width=100, height=30)
        y1 += ydiff
        self.L3.place(x=x1, y=y1)
        self.e3.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.L4.place(x=x1, y=y1)
        self.c4.place(x=x1 + xdiff, y=y1)
        y1 += ydiff
        self.b1.place(x=x1, y=y1,width=100,height=40)
        self.b2.place(x=x1+xdiff+10, y=y1, width=100, height=40)
        y1 += ydiff
        self.b3.place(x=x1, y=y1+10, width=100, height=40)
        self.b4.place(x=x1 + xdiff + 10, y=y1+10, width=100, height=40)
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
        try:
            qry="insert into designation values(%s,%s,%s,%s)"
            rowcount=self.curr.execute(qry , (self.e1.get(),self.e2.get(),self.e3.get(),self.v4.get()))
            self.conn.commit()
            if rowcount==1:
                messagebox.showinfo("Success","Data saved successfully",parent=self.window)
                self.Clearpage()
                self.Search_Data()
            else:
                messagebox.showwarning("Failure","Data not saved",parent=self.window)
        except Exception as e :
            messagebox.showerror("Query Error","Error while executing query"+str(e),parent=self.window)
    def UpdateData(self):
        if self.Validation()==False:
            return
        try:
            #designation_id	designation_name	designation_abb	department

            qry="update designation set designation_name=%s,designation_abb=%s,department=%s where designation_id=%s"
            rowcount=self.curr.execute(qry , (self.e2.get(),self.e3.get(),self.v4.get(),self.e1.get()))
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
                qry="delete from designation where designation_id=%s"
                rowcount=self.curr.execute(qry , (self.e1.get(),))
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
        self.v4.set(self.c4_msg)
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
            qry = "select * from  designation  where designation_id=%s"
            rowcount = self.curr.execute(qry,(empid,))
            data=self.curr.fetchone()
            self.Clearpage()
            if data:
                self.e1.insert(0,data[0])
                self.e2.insert(0, data[1])
                self.e3.insert(0, data[2])
                self.v4.set(data[3])
            else:
                messagebox.showwarning("Empty", "No Record found", parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error", "Error while executing query", parent=self.window)
    def Search_Data(self):
            try:
                qry="select * from designation where designation_name like %s"
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
        elif len(self.e3.get())<1 :
            messagebox.showwarning("Validation","Enter proper Abbreviation",parent=self.window)
            return False
        elif self.v4.get() == "Choose Department" or self.v4.get() == "No Department":
            messagebox.showwarning("Validation", "Select Department", parent=self.window)
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

if __name__=="__main__":
    temp=Tk()
    Designation_class(temp)
    temp.mainloop()











