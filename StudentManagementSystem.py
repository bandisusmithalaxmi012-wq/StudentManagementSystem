import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    course TEXT NOT NULL
)
""")
conn.commit()


# Add Student
def add_student():
    roll_no = roll_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    course = course_entry.get()

    if not roll_no or not name or not age or not course:
        messagebox.showwarning("Warning", "Please fill all fields")
        return

    try:
        cursor.execute(
            "INSERT INTO students VALUES (?, ?, ?, ?)",
            (int(roll_no), name, int(age), course)
        )
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
        clear_fields()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists")

    except ValueError:
        messagebox.showerror("Error", "Roll number and age must be numbers")


# View Students
def view_students():
    view_window = tk.Toplevel(window)
    view_window.title("All Students")
    view_window.geometry("700x400")
    view_window.configure(bg="#f2f2f2")

    tk.Label(
        view_window,
        text="ALL STUDENTS",
        font=("Arial", 16, "bold"),
        bg="#f2f2f2"
    ).pack(pady=15)

    columns = ("Roll No", "Name", "Age", "Course")

    table = ttk.Treeview(
        view_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=160)

    table.pack(fill="both", expand=True, padx=15, pady=10)

    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    for record in records:
        table.insert("", tk.END, values=record)


# Search Student
def search_student():
    search_window = tk.Toplevel(window)
    search_window.title("Search Student")
    search_window.geometry("400x280")
    search_window.configure(bg="#eaf2f8")

    tk.Label(
        search_window,
        text="SEARCH STUDENT",
        font=("Arial", 15, "bold"),
        bg="#eaf2f8"
    ).pack(pady=15)

    tk.Label(
        search_window,
        text="Enter Roll Number",
        bg="#eaf2f8"
    ).pack()

    search_entry = tk.Entry(search_window)
    search_entry.pack(pady=8)

    result_label = tk.Label(
        search_window,
        text="",
        bg="#eaf2f8",
        font=("Arial", 11)
    )
    result_label.pack(pady=15)

    def search():
        cursor.execute(
            "SELECT * FROM students WHERE roll_no=?",
            (search_entry.get(),)
        )
        record = cursor.fetchone()

        if record:
            result_label.config(
                text=f"Roll No: {record[0]}\n"
                     f"Name: {record[1]}\n"
                     f"Age: {record[2]}\n"
                     f"Course: {record[3]}"
            )
        else:
            result_label.config(text="Student not found")

    tk.Button(
        search_window,
        text="Search",
        command=search,
        bg="#3498db",
        fg="white",
        width=15
    ).pack(pady=5)


# Update Student
def update_student():
    update_window = tk.Toplevel(window)
    update_window.title("Update Student")
    update_window.geometry("400x400")
    update_window.configure(bg="#fff3cd")

    tk.Label(
        update_window,
        text="UPDATE STUDENT",
        font=("Arial", 15, "bold"),
        bg="#fff3cd"
    ).pack(pady=15)

    tk.Label(update_window, text="Roll Number", bg="#fff3cd").pack()
    update_roll = tk.Entry(update_window)
    update_roll.pack(pady=5)

    tk.Label(update_window, text="New Name", bg="#fff3cd").pack()
    update_name = tk.Entry(update_window)
    update_name.pack(pady=5)

    tk.Label(update_window, text="New Age", bg="#fff3cd").pack()
    update_age = tk.Entry(update_window)
    update_age.pack(pady=5)

    tk.Label(update_window, text="New Course", bg="#fff3cd").pack()
    update_course = tk.Entry(update_window)
    update_course.pack(pady=5)

    def update():
        if not update_roll.get() or not update_name.get() or not update_age.get() or not update_course.get():
            messagebox.showwarning("Warning", "Please fill all fields")
            return

        try:
            cursor.execute(
                "UPDATE students SET name=?, age=?, course=? WHERE roll_no=?",
                (
                    update_name.get(),
                    int(update_age.get()),
                    update_course.get(),
                    int(update_roll.get())
                )
            )
            conn.commit()

            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Student updated successfully")
                update_window.destroy()
            else:
                messagebox.showerror("Error", "Student not found")

        except ValueError:
            messagebox.showerror("Error", "Roll number and age must be numbers")

    tk.Button(
        update_window,
        text="Update",
        command=update,
        bg="#f39c12",
        fg="white",
        width=15
    ).pack(pady=15)


# Delete Student
def delete_student():
    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Student")
    delete_window.geometry("350x230")
    delete_window.configure(bg="#f8d7da")

    tk.Label(
        delete_window,
        text="DELETE STUDENT",
        font=("Arial", 15, "bold"),
        bg="#f8d7da"
    ).pack(pady=15)

    tk.Label(
        delete_window,
        text="Enter Roll Number",
        bg="#f8d7da"
    ).pack()

    delete_entry = tk.Entry(delete_window)
    delete_entry.pack(pady=8)

    def delete():
        cursor.execute(
            "DELETE FROM students WHERE roll_no=?",
            (delete_entry.get(),)
        )
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Student deleted successfully")
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Student not found")

    tk.Button(
        delete_window,
        text="Delete",
        command=delete,
        bg="#dc3545",
        fg="white",
        width=15
    ).pack(pady=15)


# Clear Fields
def clear_fields():
    roll_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)


# Exit
def exit_app():
    conn.close()
    window.destroy()


# Main Window
window = tk.Tk()
window.title("Student Management System")
window.geometry("550x650")
window.configure(bg="#d6eaf8")

tk.Label(
    window,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold"),
    bg="#d6eaf8",
    fg="#154360"
).pack(pady=25)

tk.Label(
    window,
    text="Python | Tkinter | SQLite",
    font=("Arial", 11),
    bg="#d6eaf8",
    fg="#34495e"
).pack(pady=5)


def create_field(label_text):
    tk.Label(
        window,
        text=label_text,
        font=("Arial", 11, "bold"),
        bg="#d6eaf8"
    ).pack()

    entry = tk.Entry(window, width=35, font=("Arial", 11))
    entry.pack(pady=6)
    return entry


roll_entry = create_field("Roll Number")
name_entry = create_field("Student Name")
age_entry = create_field("Age")
course_entry = create_field("Course")


tk.Button(
    window,
    text="Add Student",
    command=add_student,
    bg="#28a745",
    fg="white",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    window,
    text="View Students",
    command=view_students,
    bg="#007bff",
    fg="white",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    window,
    text="Search Student",
    command=search_student,
    bg="#17a2b8",
    fg="white",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    window,
    text="Update Student",
    command=update_student,
    bg="#ffc107",
    fg="black",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    window,
    text="Delete Student",
    command=delete_student,
    bg="#dc3545",
    fg="white",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    window,
    text="Clear Fields",
    command=clear_fields,
    bg="#6c757d",
    fg="white",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

tk.Button(
    window,
    text="Exit",
    command=exit_app,
    bg="#343a40",
    fg="white",
    width=25,
    font=("Arial", 10, "bold")
).pack(pady=5)

window.mainloop()