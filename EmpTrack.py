from tkinter import messagebox
from details import *
import pymysql
class MainClass:
    def __init__(self):
        self.databaseConnection()
        try:
            qry = "select * from user "
            rowcount = self.curr.execute(qry )
            data = self.curr.fetchone()
            if data:
                from logintextpage import LoginTextclass
                LoginTextclass()
            else:
                from Create_Admin import CreateAdminClass
                CreateAdminClass()
        except Exception as e:
            messagebox.showerror("Query Error","Error while executing query : \n"+str(e),)

    def databaseConnection(self):
        try:
            self.conn = pymysql.connect(host=myhost, user=myuser, password=mypass, db=mydb)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error","Error while connecting with database : \n"+str(e))

if __name__ == '__main__':
    MainClass()