# 📚 Library Management System

## Overview

A Library Management System developed using Python, Streamlit, and CSV files. It allows administrators, students, and teachers to manage books and borrowing records through an interactive web interface.

---

## Features

### Admin
- Login Authentication
- Dashboard
- Book Management (CRUD)
- User Management (CRUD)
- Borrow & Return Management
- Fine Management
- Reports
- Dashboard Statistics

### Student
- View Available Books
- Borrow Books
- Return Books
- View Borrow History

### Teacher
- View Available Books
- Borrow Books
- Return Books
- View Borrow History

---

## Technologies

- Python
- Streamlit
- Pandas
- CSV Dataset

---

## Folder Structure

```
Library_Management_System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── assets/
│   ├── library.png
│   └── style.css
│
├── data/
│   ├── books.csv
│   ├── users.csv
│   ├── borrowed_books.csv
│   ├── fines.csv
│   └── categories.csv
│
├── utils/
│   ├── auth.py
│   ├── dashboard.py
│   ├── dashboard_stats.py
│   ├── home.py
│   ├── books.py
│   ├── users.py
│   ├── borrow.py
│   ├── fines.py
│   ├── student.py
│   └── teacher.py
```

---

## Installation

```bash
git clone <repository-url>

cd Library_Management_System

pip install -r requirements.txt

streamlit run app.py
```

---

## Future Improvements

- Database Integration
- Email Notifications
- QR Code Scanning
- Barcode Scanner
- Online Book Reservation

---

## Author

Sanjay