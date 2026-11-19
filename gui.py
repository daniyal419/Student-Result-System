import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

# =================================
# MAIN WINDOW
# =================================

root = tk.Tk()
root.title("Student Result Management System")
root.geometry("1100x650")
root.minsize(900, 550)
root.configure(bg="#F3F6FB")

BLUE = "#2563EB"
DARK = "#1E293B"
WHITE = "#FFFFFF"
LIGHT = "#F3F6FB"
GREEN = "#16A34A"
RED = "#DC2626"

FILE_NAME = "students.json"

SUBJECTS = [
    "English",
    "Mathematics",
    "Computer",
    "Physics",
    "Islamiyat"
]

students = []


# =================================
# CALCULATE RESULT
# =================================

def calculate_result(marks):

    total = sum(marks.values())
    percentage = total / 5

    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    status = "Pass" if percentage >= 50 else "Fail"

    return total, percentage, grade, status


# =================================
# SAVE DATA
# =================================

def save_data():

    try:
        with open(FILE_NAME, "w") as file:
            json.dump(students, file, indent=4)

    except OSError as error:
        messagebox.showerror("Save Error", str(error))


# =================================
# LOAD DATA
# =================================

def load_data():

    global students

    if not os.path.exists(FILE_NAME):
        students = []
        return

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Invalid student data format.")

        students = []

        for item in data:

            if not isinstance(item, dict):
                continue

            if "id" not in item or "name" not in item:
                continue

            old_marks = item.get("marks", {})

            if not isinstance(old_marks, dict):
                old_marks = {}

            marks = {}

            for subject in SUBJECTS:
                value = old_marks.get(subject, 0)

                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not 0 <= value <= 100
                ):
                    value = 0

                marks[subject] = value

            total, percentage, grade, status = calculate_result(marks)

            students.append({
                "id": str(item["id"]),
                "name": str(item["name"]),
                "marks": marks,
                "total": total,
                "percentage": percentage,
                "grade": grade,
                "status": status
            })

    except (OSError, ValueError, json.JSONDecodeError):
        students = []
        messagebox.showerror(
            "Data Error",
            "students.json could not be read. "
            "Please check the data file."
        )


# =================================
# DASHBOARD
# =================================

def update_dashboard():

    total = len(students)

    passed = sum(
        1 for student in students
        if student["status"] == "Pass"
    )

    failed = sum(
        1 for student in students
        if student["status"] == "Fail"
    )

    total_label.config(text=str(total))
    passed_label.config(text=str(passed))
    failed_label.config(text=str(failed))


# =================================
# ADD STUDENT
# =================================

def add_student():

    window = tk.Toplevel(root)
    window.title("Add New Student")
    window.geometry("450x650")
    window.configure(bg=WHITE)
    window.resizable(False, False)

    tk.Label(
        window,
        text="Add New Student",
        font=("Arial", 21, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(pady=15)

    form = tk.Frame(window, bg=WHITE)
    form.pack(fill="x", padx=30)

    tk.Label(
        form,
        text="Student Name",
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    name_entry = tk.Entry(form, font=("Arial", 12))
    name_entry.pack(fill="x", pady=7)

    tk.Label(
        form,
        text="Student ID",
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w")

    id_entry = tk.Entry(form, font=("Arial", 12))
    id_entry.pack(fill="x", pady=7)

    tk.Label(
        form,
        text="Subject Marks (0-100)",
        font=("Arial", 12, "bold"),
        bg=WHITE,
        fg=DARK
    ).pack(anchor="w", pady=10)

    mark_entries = {}

    for subject in SUBJECTS:

        tk.Label(
            form,
            text=subject,
            bg=WHITE,
            fg=DARK
        ).pack(anchor="w")

        entry = tk.Entry(form, font=("Arial", 11))
        entry.pack(fill="x", pady=4)

        mark_entries[subject] = entry

    def save_student():

        name = name_entry.get().strip()
        student_id = id_entry.get().strip()

        if not name or not student_id:
            messagebox.showwarning(
                "Missing Information",
                "Please enter student name and ID.",
                parent=window
            )
            return

        if any(s["id"] == student_id for s in students):
            messagebox.showwarning(
                "Duplicate ID",
                "This Student ID already exists.",
                parent=window
            )
            return

        marks = {}

        try:
            for subject, entry in mark_entries.items():

                value = entry.get().strip()

                if not value:
                    raise ValueError(
                        f"Enter marks for {subject}."
                    )

                mark = float(value)

                if not mark.is_integer():
                    raise ValueError(
                        "Please enter whole-number marks."
                    )

                mark = int(mark)

                if mark < 0 or mark > 100:
                    raise ValueError(
                        f"{subject} marks must be between 0 and 100."
                    )

                marks[subject] = mark

        except ValueError as error:
            messagebox.showwarning(
                "Invalid Marks",
                str(error),
                parent=window
            )
            return

        total, percentage, grade, status = calculate_result(marks)

        student = {
            "id": student_id,
            "name": name,
            "marks": marks,
            "total": total,
            "percentage": percentage,
            "grade": grade,
            "status": status
        }

        students.append(student)

        save_data()
        update_dashboard()

        messagebox.showinfo(
            "Student Added",
            f"Name: {name}\n"
            f"Total: {total}/500\n"
            f"Percentage: {percentage:.2f}%\n"
            f"Grade: {grade}\n"
            f"Status: {status}",
            parent=window
        )

        window.destroy()

    tk.Button(
        window,
        text="Save Student",
        bg=BLUE,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        relief="flat",
        padx=20,
        pady=10,
        command=save_student
    ).pack(pady=15)


# =================================
# CREATE TABLE
# =================================

def create_table(window, columns, headings):

    frame = tk.Frame(window, bg=WHITE)
    frame.pack(fill="both", expand=True, padx=15, pady=10)

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for column, heading in zip(columns, headings):

        table.heading(column, text=heading)
        table.column(column, width=120, anchor="center")

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=table.yview
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return table


# =================================
# VIEW STUDENTS
# =================================

def view_students():

    window = tk.Toplevel(root)
    window.title("View Students")
    window.geometry("850x450")
    window.configure(bg=LIGHT)

    tk.Label(
        window,
        text="All Students",
        font=("Arial", 21, "bold"),
        bg=LIGHT,
        fg=DARK
    ).pack(pady=15)

    columns = (
        "id", "name", "total",
        "percentage", "grade", "status"
    )

    headings = (
        "Student ID", "Name", "Total",
        "Percentage", "Grade", "Status"
    )

    table = create_table(window, columns, headings)

    for student in students:

        table.insert(
            "",
            "end",
            values=(
                student["id"],
                student["name"],
                f'{student["total"]}/500',
                f'{student["percentage"]:.2f}%',
                student["grade"],
                student["status"]
            )
        )

    if not students:
        tk.Label(
            window,
            text="No students available.",
            bg=LIGHT,
            fg=DARK
        ).pack(pady=10)


# =================================
# SEARCH STUDENT
# =================================

def search_student():

    student_id = simpledialog.askstring(
        "Search Student",
        "Enter Student ID:",
        parent=root
    )

    if student_id is None:
        return

    student_id = student_id.strip()

    for student in students:

        if student["id"] == student_id:

            marks_text = "\n".join(
                f"{subject}: {student['marks'][subject]}"
                for subject in SUBJECTS
            )

            messagebox.showinfo(
                "Student Found",
                f"Name: {student['name']}\n"
                f"ID: {student['id']}\n\n"
                f"{marks_text}\n\n"
                f"Total: {student['total']}/500\n"
                f"Percentage: {student['percentage']:.2f}%\n"
                f"Grade: {student['grade']}\n"
                f"Status: {student['status']}"
            )

            return

    messagebox.showwarning(
        "Not Found",
        "Student ID not found."
    )


# =================================
# RESULTS
# =================================

def show_results():

    window = tk.Toplevel(root)
    window.title("Student Results")
    window.geometry("850x450")
    window.configure(bg=LIGHT)

    tk.Label(
        window,
        text="Student Results",
        font=("Arial", 21, "bold"),
        bg=LIGHT,
        fg=DARK
    ).pack(pady=15)

    columns = (
        "id", "name", "total",
        "percentage", "grade", "status"
    )

    headings = (
        "Student ID", "Name", "Total",
        "Percentage", "Grade", "Status"
    )

    table = create_table(window, columns, headings)

    for student in students:

        table.insert(
            "",
            "end",
            values=(
                student["id"],
                student["name"],
                f'{student["total"]}/500',
                f'{student["percentage"]:.2f}%',
                student["grade"],
                student["status"]
            )
        )


# =================================
# DELETE STUDENT
# =================================

def delete_student():

    student_id = simpledialog.askstring(
        "Delete Student",
        "Enter Student ID:",
        parent=root
    )

    if student_id is None:
        return

    student_id = student_id.strip()

    for student in students:

        if student["id"] == student_id:

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Delete {student['name']}?"
            )

            if confirm:

                students.remove(student)

                save_data()
                update_dashboard()

                messagebox.showinfo(
                    "Success",
                    "Student deleted successfully."
                )

            return

    messagebox.showwarning(
        "Not Found",
        "Student ID not found."
    )


# =================================
# SETTINGS
# =================================

def show_settings():

    messagebox.showinfo(
        "Settings",
        "Student Result Management System\n"
        "Version: 1.0\n"
        "Storage: students.json"
    )


# =================================
# LOAD DATA
# =================================

load_data()


# =================================
# SIDEBAR
# =================================

sidebar = tk.Frame(root, bg=DARK, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

tk.Label(
    sidebar,
    text="STUDENT SYSTEM",
    bg=DARK,
    fg=WHITE,
    font=("Arial", 16, "bold")
).pack(pady=30)


# =================================
# MAIN CONTENT
# =================================

content = tk.Frame(root, bg=LIGHT)
content.pack(
    side="left",
    fill="both",
    expand=True,
    padx=30,
    pady=25
)

tk.Label(
    content,
    text="Dashboard",
    bg=LIGHT,
    fg=DARK,
    font=("Arial", 25, "bold")
).pack(anchor="w")

tk.Label(
    content,
    text="Welcome to Student Result Management System",
    bg=LIGHT,
    fg="#64748B",
    font=("Arial", 12)
).pack(anchor="w", pady=8)


# =================================
# STATISTICS CARDS
# =================================

cards = tk.Frame(content, bg=LIGHT)
cards.pack(fill="x", pady=30)


def create_card(title, color):

    card = tk.Frame(
        cards,
        bg=WHITE,
        padx=20,
        pady=25
    )

    card.pack(
        side="left",
        expand=True,
        fill="x",
        padx=8
    )

    tk.Label(
        card,
        text=title,
        bg=WHITE,
        fg="#64748B",
        font=("Arial", 11)
    ).pack(anchor="w")

    value = tk.Label(
        card,
        text="0",
        bg=WHITE,
        fg=color,
        font=("Arial", 25, "bold")
    )

    value.pack(anchor="w", pady=8)

    return value


total_label = create_card("Total Students", BLUE)
passed_label = create_card("Passed Students", GREEN)
failed_label = create_card("Failed Students", RED)


tk.Label(
    content,
    text="Manage students, marks and academic results.",
    bg=WHITE,
    fg=DARK,
    font=("Arial", 13),
    padx=20,
    pady=25
).pack(fill="x", pady=10)


# =================================
# SIDEBAR BUTTONS
# =================================

actions = {
    "Dashboard": update_dashboard,
    "Add Student": add_student,
    "View Students": view_students,
    "Search Student": search_student,
    "Results": show_results,
    "Delete Student": delete_student,
    "Settings": show_settings
}

for name, action in actions.items():

    tk.Button(
        sidebar,
        text=name,
        bg=DARK,
        fg=WHITE,
        activebackground=BLUE,
        activeforeground=WHITE,
        font=("Arial", 12),
        relief="flat",
        anchor="w",
        padx=20,
        command=action
    ).pack(fill="x", pady=8)


# =================================
# START APPLICATION
# =================================

update_dashboard()

root.mainloop()