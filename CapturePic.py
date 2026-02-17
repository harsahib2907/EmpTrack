import tkinter as tk
import cv2
from PIL import Image, ImageTk


class CaptureClass:
    def __init__(self, pwindow):
        self.window = tk.Toplevel(pwindow)
        # self.window = tk.Tk()
        self.window.title("Login")
        self.window.protocol("WM_DELETE_WINDOW", self.capture_photo)

        self.window.attributes('-topmost', True)
        # ------------------- setting -------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        w1 = int(w / 2)
        h1 = int(h / 2) + 170
        self.window.minsize(w1, h1)
        self.window.geometry("%dx%d+%d+%d" % (w1, h1, int(w1 / 2), int(h1 / 2) - 150))  # width,height,x,y
        myfont1 =  'Cambria',16,'bold'
        mycolor1 = '#bad1e8'
        mycolor2='black'
        mycolor3='#6A89A7'
        # self.window.config(background=mycolor1)
        self.headlbl = tk.Label(self.window, text="Get Picture", font=('Book Antiqua', 26, 'bold'),
                               background=mycolor3,foreground=mycolor1, relief='groove', borderwidth=5)


        # --------------- buttons ---------------------------
        self.b1 = tk.Button(self.window, text="Click",background=mycolor3,foreground=mycolor1,font=myfont1, command=self.capture_photo)

        btn_height = 40
        self.canvas_height = h1 - (70 + btn_height)
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
        # frame = cv2.cvtColor(frame, cv2.COLOR_LAB2BGR)
        frame = cv2.resize(frame, (self.canvas_width, self.canvas_height))
        img = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=img)
        return photo


    def capture_photo(self):
        ret, frame = self.vid.read()
        if ret:
            # Save the captured frame as an image file
            cv2.imwrite("captured_photo.jpg", frame)
        self.vid.release()
        self.window.destroy()

if __name__ == '__main__':
    dummy = tk.Tk()
    CaptureClass(dummy)
    dummy.mainloop()
