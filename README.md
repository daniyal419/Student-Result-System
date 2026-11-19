# Student Result Management System

A beginner-friendly Python console project for managing student marks and results.

## Features

- Add a student with a unique student ID
- Enter and validate marks for five subjects
- Automatically calculate total, percentage, grade, and pass/fail status
- View all student records
- Search for a student by ID
- Delete a student record
- View class statistics and the top student
- Save records automatically in a JSON file

## Technologies

- Python 3
- JSON file handling
- Functions, lists, dictionaries, loops, and conditional statements

## Requirements

- Python 3.8 or newer
- No external libraries are required

## How to Run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

The program creates `students.json` automatically when the first student is added.

## Grading Rules

| Percentage | Grade |
|---|---|
| 90–100 | A+ |
| 80–89.99 | A |
| 70–79.99 | B |
| 60–69.99 | C |
| 50–59.99 | D |
| Below 50 | F |

A student passes with a percentage of 50 or above.

## Project Structure

```text
student-result-management-system/
├── main.py
├── README.md
└── .gitignore
```

## Learning Outcomes

This project demonstrates:
- Breaking a program into reusable functions
- Validating user input
- Working with lists and dictionaries
- Reading and writing JSON data
- Searching and deleting records
- Calculating summaries from stored data

## Future Improvements

- Add a graphical user interface
- Export reports to CSV
- Add student record editing
- Add login functionality

## Author

Add your name here before publishing.
## Project Screenshot
![Student Result Management System]
(project-screenshot.png)
