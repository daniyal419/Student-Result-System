"""
Student Result Management System
A beginner-friendly Python project using functions, lists, dictionaries, JSON, and file handling.
Run: python main.py
"""

import json
import os

DATA_FILE = "students.json"


def load_students():
    """Load saved student records from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data. Starting with an empty list.")
        return []


def save_students(students):
    """Save student records so they remain available next time."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)


def calculate_result(marks):
    total = sum(marks)
    percentage = total / len(marks)

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


def get_valid_marks():
    """Ask for five marks and validate each value."""
    marks = []
    subjects = ["English", "Mathematics", "Computer", "Physics", "Islamiyat"]

    for subject in subjects:
        while True:
            try:
                mark = float(input(f"Enter marks for {subject} (0-100): "))
                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                print("Marks must be between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")

    return marks


def add_student(students):
    print("\n--- Add New Student ---")
    student_id = input("Enter student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if any(student["id"].lower() == student_id.lower() for student in students):
        print("A student with this ID already exists.")
        return

    name = input("Enter student name: ").strip()
    if not name:
        print("Student name cannot be empty.")
        return

    marks = get_valid_marks()
    total, percentage, grade, status = calculate_result(marks)

    students.append({
        "id": student_id,
        "name": name,
        "marks": marks,
        "total": total,
        "percentage": round(percentage, 2),
        "grade": grade,
        "status": status
    })
    save_students(students)
    print(f"\nRecord saved successfully. Grade: {grade} | Result: {status}")


def view_students(students):
    print("\n--- All Student Records ---")
    if not students:
        print("No student records found.")
        return

    print(f"{'ID':<12}{'Name':<22}{'Total':<10}{'Percent':<12}{'Grade':<8}{'Result'}")
    print("-" * 75)
    for student in students:
        print(
            f"{student['id']:<12}{student['name']:<22}"
            f"{student['total']:<10.1f}{student['percentage']:<12.2f}"
            f"{student['grade']:<8}{student['status']}"
        )


def search_student(students):
    print("\n--- Search Student ---")
    search_id = input("Enter student ID: ").strip().lower()

    for student in students:
        if student["id"].lower() == search_id:
            print(f"\nName: {student['name']}")
            print(f"ID: {student['id']}")
            print(f"Marks: {student['marks']}")
            print(f"Total: {student['total']} / 500")
            print(f"Percentage: {student['percentage']}%")
            print(f"Grade: {student['grade']}")
            print(f"Result: {student['status']}")
            return

    print("Student not found.")


def delete_student(students):
    print("\n--- Delete Student ---")
    student_id = input("Enter student ID to delete: ").strip().lower()

    for index, student in enumerate(students):
        if student["id"].lower() == student_id:
            confirm = input(f"Delete {student['name']}'s record? (y/n): ").strip().lower()
            if confirm == "y":
                students.pop(index)
                save_students(students)
                print("Student record deleted.")
            else:
                print("Delete cancelled.")
            return

    print("Student not found.")


def show_class_summary(students):
    print("\n--- Class Summary ---")
    if not students:
        print("No records available for summary.")
        return

    average = sum(s["percentage"] for s in students) / len(students)
    passed = sum(1 for s in students if s["status"] == "Pass")
    failed = len(students) - passed
    topper = max(students, key=lambda s: s["percentage"])

    print(f"Total students: {len(students)}")
    print(f"Class average: {average:.2f}%")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Top student: {topper['name']} ({topper['percentage']}%)")


def show_menu():
    print("\n" + "=" * 42)
    print("       STUDENT RESULT MANAGEMENT")
    print("=" * 42)
    print("1. Add student")
    print("2. View all students")
    print("3. Search student")
    print("4. Delete student")
    print("5. Class summary")
    print("0. Exit")
    print("-" * 42)


def main():
    students = load_students()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            show_class_summary(students)
        elif choice == "0":
            print("Thank you for using Student Result Management System!")
            break
        else:
            print("Invalid option. Please choose from the menu.")


if __name__ == "__main__":
    main()
