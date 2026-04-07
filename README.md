# SAMSS – Student Academic Monitoring and Support System

> IST1025 – Introduction to Programming | Kenyan University Student Support System

---

## What Is SAMSS?

SAMSS is a command-line Python system built to help university departments in Kenya monitor students early and step in before academic failure occurs.

At many Kenyan universities, students face challenges tracking their academic performance, managing attendance, and understanding what they need to progress. SAMSS solves this by giving departments a single tool that registers students, tracks their scores and attendance, calculates grades and risk levels automatically, and saves all records so nothing is lost between sessions.

---

## Features

- Register students with their ID, name, units, scores and attendance
- Automatically compute the average score across all units
- Classify grades using the Kenyan university grading scale (A to E)
- Determine academic risk level — Low, Moderate or High — based on score and attendance
- Validate all user input — rejects blank names, wrong number types, out-of-range scores
- Save and load all records from a JSON file so data persists between sessions
- Menu-driven interface with 7 options — no commands to memorise
- At-risk report showing only students who need attention
- Class statistics — total students, class average, top and lowest performer
- Scholarship eligibility checker — automatically identifies qualifying students

---

## Grading Scale

| Grade | Score Range | Classification     |
|-------|-------------|-------------------|
| A     | 70 and above | First Class        |
| B     | 60 – 69      | Upper Second       |
| C     | 50 – 59      | Lower Second       |
| D     | 40 – 49      | Pass               |
| E     | Below 40     | Fail               |

---

## Academic Risk Levels

| Risk Level | Condition                                              |
|------------|--------------------------------------------------------|
| High       | Average below 40, OR average below 50 with attendance below 60% |
| Moderate   | Average below 55, OR attendance below 75%             |
| Low        | Performing well in both score and attendance           |

---

## How to Run

Make sure you have Python 3 installed. Then:

```bash
python samss.py
```

That's it. No libraries to install — SAMSS only uses `json` and `os` which are built into Python.

---

## Menu Options

```
==========================================
  SAMSS - Student Monitoring System
==========================================
  1. Register a new student
  2. View a student report
  3. List all students
  4. Update a student record
  5. Delete a student record
  6. Show at-risk students
  7. Show class statistics
  8. Check scholarship eligibility
  0. Exit
==========================================
```

---

## Project Structure

```
SAMSS-IST1025/
│
├── samss.py          # Main Python program — all code is here
├── students.json     # Auto-created when first student is registered
└── README.md         # This file
```

---

## System Design

SAMSS is split into clearly labelled modules, each with one specific job:

| Module | Functions | What It Does |
|--------|-----------|--------------|
| Student Class | `__init__`, `get_scores`, `to_dict` | Stores all student data as one object |
| File Functions | `load_students`, `save_students` | Reads and writes records to students.json |
| Calculation Functions | `compute_average`, `get_grade`, `get_risk_level` | All maths and logic — no input or print inside |
| Validation Functions | `get_valid_name`, `get_valid_int`, `get_valid_score` | Validates all user input before it is used |
| Display Functions | `print_student_report`, `print_all_students` | Formats and prints results to the screen |
| Menu Functions | `register_student`, `view_student`, etc. | Connects input, logic and display together |
| Main Program | `show_menu`, `main` | Runs the menu loop and calls the right function |

---

## Edge Cases Handled

| Edge Case | How It Is Handled |
|-----------|------------------|
| User types letters where a number is expected | `try/except ValueError` catches it and re-prompts |
| Score entered below 0 or above 100 | Range check with clear error message |
| Name or ID left blank | Checks for empty string before accepting |
| Duplicate student ID on registration | Checks dictionary before adding |
| Student ID not found when searching | Guard clause with error message |
| Save file missing or broken on startup | `try/except` returns empty dict, program continues |
| No students registered when viewing reports | Empty dictionary check with message |

---

## Data File

Student records are stored in `students.json` which is created automatically when the first student is registered. It is saved after every change and loaded when the program opens.

Example structure:
```json
{
    "KU/2024/001": {
        "name": "Alice Wanjiru",
        "units": [
            {"unit_name": "MAT101", "score": 78.0},
            {"unit_name": "ENG102", "score": 65.5}
        ],
        "attendance": 85.0
    }
}
```

---

## Course Information

- **Course:** IST1025 – Introduction to Programming
- **Institution:** United States International University – Africa (USIU-Africa)
- **Project:** Student Academic Monitoring and Support System (SAMSS)
- **Language:** Python 3

---

## Author

USIU-Africa Student | IST1025 Coursework Submission
