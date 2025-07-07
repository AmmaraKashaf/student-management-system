import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# 1. Database Setup
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
)
""")
conn.commit()
# Create Grades Table (NEW PART)
cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT NOT NULL,
    score INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
""")
conn.commit()

def add_grade(student_id, subject, score):
    try:
        cursor.execute("INSERT INTO grades (student_id, subject, score) VALUES (?, ?, ?)", (student_id, subject, score))
        conn.commit()

        # Log the change
        with open("grades.log", "a") as log_file:
            log_file.write(f"Student ID {student_id} - {subject}: {score}\n")

        print("Grade added and logged!")
    except Exception as e:
        print("Error adding grade:", e)

# 2. GUI Functions
def add_student():
    name = name_entry.get()
    email = email_entry.get()
    if name and email:
        try:
            cursor.execute("INSERT INTO students (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student Added!")
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
    else:
        messagebox.showerror("Error", "Name/Email cannot be empty!")

def view_students():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    for student in students:
        print(student)  # Terminal mein dikhega

# 3. Main Window
root = tk.Tk()
root.title("Student Management System")
root.geometry("400x300")

# Labels & Entries
tk.Label(root, text="Name:").place(x=20, y=20)
name_entry = tk.Entry(root, width=30)
name_entry.place(x=100, y=20)

tk.Label(root, text="Email:").place(x=20, y=50)
email_entry = tk.Entry(root, width=30)
email_entry.place(x=100, y=50)

# Buttons
tk.Button(root, text="Add Student", command=add_student).place(x=100, y=90)
tk.Button(root, text="View Students", command=view_students).place(x=200, y=90)

root.mainloop()
def export_to_csv(filename="students_export.csv"):
    import sqlite3
    import csv

    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT students.id, students.name, students.email, grades.subject, grades.score
    FROM students
    LEFT JOIN grades ON students.id = grades.student_id
    ORDER BY students.id
    """)
    rows = cursor.fetchall()

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Student ID", "Name", "Email", "Subject", "Score"])
        writer.writerows(rows)

    print(f"Data exported to {filename}")
root = tk.Tk()
root.title("Student Management System")
...
root.mainloop()
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Student Management System")
    root.geometry("400x300")

    # Labels & Entries
    tk.Label(root, text="Name:").place(x=20, y=20)
    name_entry = tk.Entry(root, width=30)
    name_entry.place(x=100, y=20)

    tk.Label(root, text="Email:").place(x=20, y=50)
    email_entry = tk.Entry(root, width=30)
    email_entry.place(x=100, y=50)

    # Buttons
    tk.Button(root, text="Add Student", command=add_student).place(x=100, y=90)
    tk.Button(root, text="View Students", command=view_students).place(x=200, y=90)

    root.mainloop()
