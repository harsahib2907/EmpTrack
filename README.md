# EmpTrack 👥

A desktop-based **Employee Management & Tracking System** built with Python and Tkinter. EmpTrack provides HR teams and administrators with a centralised platform to manage employees, track attendance, handle leave requests, monitor salary records, and generate reports — all secured with dual login options including **facial recognition**.

---

## ✨ Features

- **Dual Authentication** — Log in via face recognition (powered by `dlib` & OpenCV) or traditional username/password
- **Employee Management** — Add, update, and delete employee records with photo capture
- **Attendance Tracking** — Mark and view attendance logs with timestamped records
- **Leave Management** — Submit, approve, and track employee leave requests
- **Department & Designation Management** — Organise employees by department and job title
- **Salary Records** — Maintain and view salary details per employee
- **Performance Reviews** — Record and retrieve employee review/appraisal data
- **Date of Birth Records** — Store and access employee DOB information
- **PDF Report Generation** — Export records and reports as printable PDFs
- **Admin Panel** — Create and manage admin accounts with role-based access
- **Password Management** — Secure in-app password change functionality

---

## 🗂️ Project Structure

```
EmpTrack/
│
├── main.py                  # Application entry point
├── homepage.py              # Main dashboard/home screen
│
├── # Authentication
├── faceloginpage.py         # Face recognition login screen
├── logintextpage.py         # Username/password login screen
├── CapturePic.py            # Webcam photo capture utility
├── Create_Admin.py          # Admin account creation
├── change_password.py       # Password change module
│
├── # Core Modules
├── EmpTrack.py              # Core application logic
├── employee_manger.py       # Employee CRUD operations
├── details.py               # Employee detail view
├── departments.py           # Department management UI
├── designation.py           # Designation management UI
│
├── # Records & Tracking
├── attendence_tracker.py    # Attendance tracking module
├── LeaveTracker.py          # Leave request & approval module
├── record.py                # General records handler
├── record_department.py     # Department-wise records
├── record_salary.py         # Salary record management
├── record_dob.py            # Date of birth records
│
├── # Reviews & Reports
├── review.py                # Employee performance review entry
├── review_record.py         # Review records viewer
├── Print.py                 # PDF print/export utility
│
├── # Database
├── emp_track_db.sql         # MySQL database schema & seed data
│
├── # Assets
├── Emp_Images/              # Employee profile images
├── User_Img/                # User account images
├── app_image/               # Application UI assets
├── captured_photo.jpg       # Temporary webcam capture
│
└── dlib-19.22.99-cp39-cp39-win_amd64.whl  # Pre-built dlib wheel for Windows
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.9 |
| GUI Framework | Tkinter |
| Face Recognition | dlib, OpenCV, face_recognition |
| Database | MySQL |
| PDF Generation | ReportLab / fpdf |
| Image Handling | Pillow (PIL) |

---

## ⚙️ Prerequisites

- Python 3.9 (recommended for dlib compatibility)
- MySQL Server
- A working webcam (for face recognition login)

---

## 🚀 Installation & Setup

**1. Clone the repository**

```bash
git clone https://github.com/harsahib2907/EmpTrack.git
cd EmpTrack
```

**2. Install dlib**

A pre-built Windows wheel is included for Python 3.9:

```bash
pip install dlib-19.22.99-cp39-cp39-win_amd64.whl
```

> On Linux/macOS, install dlib via: `pip install dlib`

**3. Install remaining dependencies**

```bash
pip install opencv-python face_recognition Pillow mysql-connector-python reportlab
```

**4. Set up the database**

Import the provided SQL schema into your MySQL server:

```bash
mysql -u root -p < emp_track_db.sql
```

Then update your database credentials in the relevant config section of `EmpTrack.py`.

**5. Create an admin account**

```bash
python Create_Admin.py
```

**6. Run the application**

```bash
python main.py
```

---

## 🖥️ Usage

1. Launch the app with `python main.py`
2. Choose your login method — **Face Recognition** or **Text Login**
3. Once authenticated, the dashboard provides access to all modules: employees, attendance, leaves, departments, salary, reviews, and reports
4. Admins can manage all records and generate PDF reports via the Print module

---

## 📸 Screenshots

> Screenshots can be found in the `app_image/` directory.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source. Feel free to use and modify it for educational or personal purposes.

---

## 👨‍💻 Author

**harsahib2907** — [GitHub Profile](https://github.com/harsahib2907)
