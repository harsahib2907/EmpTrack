import os
import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
import pymysql
from PIL import Image, ImageTk
from details import *

class FaceLoginClass:
    folder='User_Img'
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.protocol("WM_DELETE_WINDOW", self.quit)
        self.window.attributes('-topmost', True)
        #------------------- setting -------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        w1 = int(w/2)
        h1 = int(h/2)+170
        self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1,h1 ,int(w1/2),int(h1/2)-150)) # width,height,x,y


        # self.window.config(background=mycolor1)
        self.headlbl = tk.Label(self.window, text="Welcome to "+app_name, font=headingfont,
        background=mycolor2, foreground=mycolor4, relief='groove', borderwidth=5)

        self.L1 = tk.Label(self.window, text="- - -", font=myfont1,background=mycolor3,foreground=mycolor1)

        # --------------- buttons ---------------------------
        self.b1 = tk.Button(self.window, text="Login",background=mycolor3,foreground=mycolor1, font=myfont1,command=self.CheckFace)
        self.b2 = tk.Button(self.window, text="Try Another Way",background=mycolor3,foreground=mycolor1, font=myfont1,command=self.openanotherway)

        btn_height = 40
        self.canvas_height = h1 - (70 + btn_height * 3)
        self.canvas_width = w1
        self.canvas = tk.Canvas(self.window, width=self.canvas_width,
                                height=self.canvas_height, background='pink')

        # --------------- placements -----------------------------
        self.headlbl.place(x=0, y=0, width=w1, height=70)
        x1 = 0
        y1 = 100
        x_diff = 150
        y_diff = 40
        self.canvas.place(x=0, y=70)
        y1 = self.canvas_height + 70
        self.b1.place(x=0, y=y1, width=w1, height=btn_height)
        y1 += y_diff
        self.L1.place(x=x1, y=y1, width=w1, height=btn_height)
        y1 += y_diff
        self.b2.place(x=x1, y=y1, width=w1, height=btn_height)

        self.databaseConnection()


        #check eacvh photo from folder and make their encodings
        images_list = os.listdir(self.folder)
        self.known_face_encoding = []
        self.known_faces_names = []
        for img_name in images_list:
            print(img_name)
            selected_image = face_recognition.load_image_file(self.folder + "/" + img_name)
            s_encoding = face_recognition.face_encodings(selected_image)
            if not s_encoding:
                continue # skip if given image is not recoginizable
            selected_encoding = s_encoding[0]
            self.known_face_encoding.append(selected_encoding)
            # self.known_faces_names.append(img_name.split(".")[0])
            self.known_faces_names.append(img_name)

        # print("All Names List = ", self.known_faces_names)


        self.vid = cv2.VideoCapture(0)
        self.update()
        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = self.convert_frame_to_photo(frame)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def convert_frame_to_photo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo


    def quit(self):
        self.vid.release()
        self.window.destroy()

    def openanotherway(self):
        self.quit()
        from logintextpage import LoginTextclass
        LoginTextclass()

    def CheckFace(self):
        ret, frame = self.vid.read()
        curr_face_locations = face_recognition.face_locations(frame)
        curr_face_encodings = face_recognition.face_encodings(frame, curr_face_locations)
        for face_encoding in curr_face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encoding, face_encoding)
            name = ""
            face_distance = face_recognition.face_distance(self.known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = self.known_faces_names[best_match_index]
                if name in self.known_faces_names:
                    self.L1.config(text='Face Found ')
                    self.img_name = name
                    self.checkData()
                    return
        self.L1.config(text='Not Known Face')




    def databaseConnection(self):
        try:
            self.conn = pymysql.connect(host=myhost, user=myuser, password=mypass, db=mydb)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e),parent=self.window)

    def checkData(self):
        try:
            qry = "select * from user where user_pic =%s"
            rowcount = self.curr.execute(qry ,(self.img_name))
            data = self.curr.fetchone()
            if data:
                uname = data[0]
                utype = data[2]
                messagebox.showinfo(f"Success ",f"Welcome {uname} [{utype}]",parent=self.window)

                self.quit()

                from homepage import Homeclass
                Homeclass(uname,utype)
            else:
                messagebox.showerror("Empty ","Image Present But No record Present",parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error ","Error while saving data :\n"+str(e),parent=self.window)

if __name__ == '__main__':
    FaceLoginClass()