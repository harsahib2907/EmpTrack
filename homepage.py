from tkinter import *
from tkinter import messagebox

from details import *


from employee_manger import Employee_class
from record import Record_class
from departments import Department_class
from designation import Designation_class
from record_department import Record2_class
from record_dob import Record3_class
from record_salary import Record4_class
from user import User_class
from change_password import Change_Password_class
from attendence_tracker import Attendence_class
from LeaveTracker import Leave_Tracker_class
from review import  Review_class
from review_record import Review_Record_class


from PIL import Image,ImageTk
class Homeclass:
    def __init__(self,un,ut):
        self.utype=ut
        self.uname=un
        self.window=Tk()
        #-----------------------Settings-------------------
        w=self.window.winfo_screenwidth()
        h=self.window.winfo_screenheight()
        s_w1=w//2
        s_h1=h//2
        s_x1=w//4
        s_y1=h//4
        self.window.minsize(s_w1,s_h1)
        self.window.geometry("%dx%d+%d+%d"%(s_w1,s_h1,s_x1,s_y1))
        self.window.state("zoomed")

        hd_height = 100
        frame_width = 250
        #-----------------Frames---------------
        self.heading=Label(self.window,text=app_name,background=mycolor1,foreground=mycolor4,font=headingfont)
        self.f1=Frame(self.window,background=mycolor3)
        self.bg_img = ImageTk.PhotoImage(Image.open("app_image//bg.jpg").resize((w - frame_width, h - hd_height)))
        self.img=Label(self.window,image=self.bg_img,background=mycolor2,foreground=mycolor4)

        self.heading.place(x=0,y=0,width=w,height=hd_height)
        self.f1.place(x=0,y=hd_height,width=frame_width,height=h-hd_height)

        self.img.place(x=frame_width,y=hd_height,width=w-frame_width,height=h-hd_height)
        #----------------Buttons------------------
        x1,y1=1,0
        b_w=frame_width-2
        b_h=50
        y_diff=b_h+5
        self.emp_img = ImageTk.PhotoImage(Image.open("app_image//emp1.png").resize((50,40)))
        self.b1=Button(self.f1,text="Employee Manger",background=mycolor2,foreground=mycolor4,font=subheadingfont,command= lambda : Employee_class(self.window),image=self.emp_img,compound=LEFT)
        self.b1.place(x=x1,y=y1,width=b_w,height=b_h)
        if self.utype == "Admin":
            y1 += y_diff
            self.user_img = ImageTk.PhotoImage(Image.open("app_image//user.png").resize((50, 40)))
            self.b2 = Button(self.f1, text="USERS", background=mycolor2, foreground=mycolor4,
                             font=subheadingfont, command=lambda: User_class(self.window), image=self.user_img,
                             compound=LEFT)
            self.b2.place(x=x1, y=y1, width=b_w, height=b_h)
            y1 += y_diff
            self.review_img = ImageTk.PhotoImage(Image.open("app_image//review.png").resize((50, 40)))
            self.b14 = Button(self.f1, text="Employee Review \nTracker", background=mycolor2, foreground=mycolor4,
                             font=subheadingfont, command=lambda: Review_Record_class(self.window), image=self.review_img,
                             compound=LEFT)
            self.b14.place(x=x1, y=y1, width=b_w, height=b_h)
        if self.utype=="HR":
            y1 += y_diff
            self.attendence_img = ImageTk.PhotoImage(Image.open("app_image//attendence.png").resize((50, 40)))
            self.b3 = Button(self.f1, text="Attendance Tracker", background=mycolor2, foreground=mycolor4,
                             font=subheadingfont, command=lambda: Attendence_class(self.window), image=self.attendence_img,
                             compound=LEFT)
            self.b3.place(x=x1, y=y1, width=b_w, height=b_h)
            y1 += y_diff
            self.leave_img = ImageTk.PhotoImage(Image.open("app_image//leave.png").resize((50, 40)))
            self.b12 = Button(self.f1, text="Leave Tracker", background=mycolor2, foreground=mycolor4,
                             font=subheadingfont, command=lambda: Leave_Tracker_class(self.window),
                             image=self.leave_img,
                             compound=LEFT)
            self.b12.place(x=x1, y=y1, width=b_w, height=b_h)
            y1 += y_diff
            self.review_img = ImageTk.PhotoImage(Image.open("app_image//review.png").resize((50, 40)))
            self.b13 = Button(self.f1, text="Employee Review", background=mycolor2, foreground=mycolor4,
                             font=subheadingfont, command=lambda: Review_class(self.window),
                             image=self.review_img,
                             compound=LEFT)
            self.b13.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.department_img = ImageTk.PhotoImage(Image.open("app_image//department.png").resize((50, 40)))
        self.b4 = Button(self.f1, text="Departments", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda: Department_class(self.window), image=self.department_img,
                         compound=LEFT)
        self.b4.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.designation_img = ImageTk.PhotoImage(Image.open("app_image//designation.png").resize((50, 40)))
        self.b5 = Button(self.f1, text="Designation", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda: Designation_class(self.window), image=self.designation_img,
                         compound=LEFT)
        self.b5.place(x=x1, y=y1, width=b_w, height=b_h)
        # if self.utype == "Admin":
        y1+=y_diff
        self.rec_img = ImageTk.PhotoImage(Image.open("app_image//record.png").resize((50, 40)))
        self.b6 = Button(self.f1, text="Employee Record", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda: Record_class(self.window), image=self.rec_img,
                         compound=LEFT)
        self.b6.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.rec_sub1_img = ImageTk.PhotoImage(Image.open("app_image//record_sub.png").resize((50, 40)))
        self.b7 = Button(self.f1, text="Record by \nDepartments", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda: Record2_class(self.window), image=self.rec_sub1_img,
                         compound=LEFT)
        self.b7.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.rec_sub2_img = ImageTk.PhotoImage(Image.open("app_image//record_sub.png").resize((50, 40)))
        self.b8 = Button(self.f1, text="Record by \nDOB", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda: Record3_class(self.window), image=self.rec_sub2_img,
                         compound=LEFT)
        self.b8.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.rec_sub3_img = ImageTk.PhotoImage(Image.open("app_image//record_sub.png").resize((50, 40)))
        self.b9 = Button(self.f1, text="Record by \nSalaries", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda: Record4_class(self.window), image=self.rec_sub3_img,
                         compound=LEFT)
        self.b9.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.changepass_img = ImageTk.PhotoImage(Image.open("app_image//change_password.png").resize((50, 40)))
        self.b10 = Button(self.f1, text="Change Password", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=lambda:Change_Password_class(self.window,self.uname), image=self.changepass_img,
                         compound=LEFT)
        self.b10.place(x=x1, y=y1, width=b_w, height=b_h)
        y1 += y_diff
        self.logout_img = ImageTk.PhotoImage(Image.open("app_image//logout.png").resize((50, 40)))
        self.b11 = Button(self.f1, text="Logout", background=mycolor2, foreground=mycolor4,
                         font=subheadingfont, command=self.quitter, image=self.logout_img,
                         compound=LEFT)
        self.b11.place(x=x1, y=y1, width=b_w, height=b_h)

        self.window.mainloop()
    def quitter(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to Logout ? ",parent=self.window)
        if ans=="yes":
            self.window.destroy()
            from logintextpage import LoginTextclass
            LoginTextclass()


if __name__ == "__main__":
    obj = Homeclass("abc","xyz")