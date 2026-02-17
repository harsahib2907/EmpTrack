import os
from fpdf import FPDF
from details import *

address="Jalandhar"
contact="98989898"

class PrintClass(FPDF):
    # def __init__(self):
    #     self.mycolor1 = 34, 40, 49
    #     self.mycolor2 = 49, 54, 63
    #     self.mycolor3 = 118, 171, 174
    #     self.mycolor4 = 238, 238, 238
    # myfont1 = "Lato"
    # myfont2 = "PT Serif"
    def header(self):
        self.set_text_color(34, 40, 49)

        self.set_font("Arial", 'B', 20)
        self.cell(0, 10, app_name, 0, 0, 'C')
        self.ln(10) # line break

        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, address, 0, 0, 'C')
        self.ln(10)

        self.cell(0, 10,contact, 0, 0, 'C')
        self.ln(10)

        self.ln(20)

    def footer(self):
        self.set_y(-15)  # Position at 1.5 cm from bottom
        self.set_font("Arial", 'I', 8)
        self.set_text_color(142, 142, 142)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C') # (width,height,text,border,line,alignment)

    def content(self,msg,tableheadings,table_data):
        self.add_page()

        # ---------- message --------------
        self.set_fill_color(238,238,238)
        self.cell(self.w-20,10, msg,0,1,'C',True) # (width,height,text,border,line,alignment,fill)
        self.ln(10)


        # --------- calculation & settings ----------------
        self.set_text_color(118, 171, 174)
        self.set_font("Arial", 'B', 11)
        spacing=2
        col_width = self.w / (len(tableheadings) +1 ) # no of columns +1 to adjust columns to screen
        row_height = self.font_size+2

        #------- table heading ----------------
        for i in tableheadings:
            self.cell(col_width, row_height * spacing, text=i, border=1)
        self.ln(row_height * spacing)

        # -------- table body -----------------
        self.set_font("Arial", '', 11)
        for row in table_data:
            for item in row:
                self.cell(col_width, row_height * spacing, text=str(item), border=1)
            self.ln(row_height * spacing) # Line break

        self.ln(10)
        self.set_font("Arial", 'I')
        text1 = '(--------------------- end of page -----------------------)'
        w = self.get_string_width(text1) + 6
        self.set_x((210 - w) / 2)
        self.cell(0, 6, text1)


if __name__ == '__main__':
    pdf = PrintClass()
    # employee_id	name		designation	department	dob	phone_number	email	address	gender	salary

    headings = ['Emp_Id', 'Name', 'Designation', 'Department', 'DOB',  'Salary']
    data=[['Emp_Id', 'Name', 'Designation', 'Department', 'DOB',  'Salary'],
          ['Emp_Id', 'Name', 'Designation', 'Department', 'DOB',  'Salary'],
          ['Emp_Id', 'Name', 'Designation', 'Department', 'DOB',  'Salary']]

    pdf.content("Employee Record",headings,data)

    pdf.output('pdf_file1.pdf')
    os.system('explorer.exe "pdf_file1.pdf"')