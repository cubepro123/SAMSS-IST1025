# ============================================================
# SAMSS - Student Academic Monitoring and Support System
# IST1025 - Introduction to Programming
# Kenyan University Student Support System
# ============================================================
#
# EDGE CASES THIS PROGRAM HANDLES:
# 1. User types letters where a number is expected (e.g "abc")
#    - Fixed using try/except so the program does not crash
# 2. Score entered is below 0 or above 100
#    - Fixed using an if statement to check the range
# 3. User leaves the name or ID blank
#    - Fixed by checking if the input is empty before accepting
# 4. Student ID already exists when registering
#    - Fixed by checking the dictionary before adding
# 5. Student ID not found when searching or deleting
#    - Fixed by checking if the ID is in the dictionary first
# 6. The save file is missing or broken when the program opens
#    - Fixed using try/except when reading the file
# 7. No students registered yet when viewing reports
#    - Fixed by checking if the dictionary is empty first
# ============================================================

import json
import os

# The file where all student records are saved
DATA_FILE = "students.json"


# ============================================================
# THE STUDENT CLASS
# ============================================================

class Student:
    """A class to represent one student in the system."""

    def __init__(self, student_id, name, units, attendance):
        """
        Set up a new Student object with their details.

        student_id  - the student's unique ID number (string)
        name        - the student's full name (string)
        units       - a list of subjects and scores (list of dicts)
        attendance  - the student's attendance percentage (float)
        """
        self.student_id = student_id
        self.name = name
        self.units = units        # e.g. [{"unit_name": "Maths", "score": 75}]
        self.attendance = attendance

    def get_scores(self):
        """Return a list of just the scores from all units."""
        scores = []
        for unit in self.units:
            scores.append(unit["score"])
        return scores

    def to_dict(self):
        """Convert the student object into a dictionary for saving."""
        return {
            "name": self.name,
            "units": self.units,
            "attendance": self.attendance
        }


# ============================================================
# FILE FUNCTIONS - saving and loading from the file
# ============================================================

def load_students():
    """
    Load all students from the save file.
    Returns an empty dictionary if the file does not exist yet.
    """
    # If no save file exists yet, just start with no students
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        file = open(DATA_FILE, "r")
        data = json.load(file)
        file.close()

        # Convert each saved dictionary back into a Student object
        students = {}
        for student_id in data:
            info = data[student_id]
            students[student_id] = Student(student_id, info["name"],
                                           info["units"], info["attendance"])
        return students

    except:
        # If the file is broken or unreadable, start fresh
        print("Warning: could not read save file. Starting with empty records.")
        return {}


def save_students(students):
    """
    Save all students to the file so records are not lost.
    Converts each Student object to a dictionary before saving.
    """
    try:
        # Build a plain dictionary we can write to JSON
        data = {}
        for student_id in students:
            data[student_id] = students[student_id].to_dict()

        file = open(DATA_FILE, "w")
        json.dump(data, file, indent=4)
        file.close()

    except:
        print("Error: could not save records to file.")


# ============================================================
# CALCULATION FUNCTIONS - the logic of the system
# (these functions do NOT use input() or print())
# ============================================================

def compute_average(scores):
    """
    Calculate and return the average of a list of scores.
    Returns 0 if the list is empty to avoid a division error.
    """
    if len(scores) == 0:
        return 0

    total = 0
    for score in scores:
        total = total + score

    average = total / len(scores)
    return round(average, 2)


def get_grade(average):
    """
    Return the letter grade and description for a given average.
    Uses the Kenyan university grading scale.

    A = 70 and above  (First Class)
    B = 60 to 69      (Upper Second)
    C = 50 to 59      (Lower Second)
    D = 40 to 49      (Pass)
    E = below 40      (Fail)
    """
    if average >= 70:
        return "A", "First Class"
    elif average >= 60:
        return "B", "Upper Second"
    elif average >= 50:
        return "C", "Lower Second"
    elif average >= 40:
        return "D", "Pass"
    else:
        return "E", "Fail"


def get_risk_level(average, attendance):
    """
    Return the academic risk level for a student.
    Uses both their average score and attendance percentage.

    High     - average below 40, or below 50 with low attendance
    Moderate - average below 55, or attendance below 75%
    Low      - doing well in both score and attendance
    """
    if average < 40 or (average < 50 and attendance < 60):
        return "High"
    elif average < 55 or attendance < 75:
        return "Moderate"
    else:
        return "Low"


# ============================================================
# INPUT VALIDATION FUNCTIONS
# (these re-ask the question until the user gives valid input)
# ============================================================

def get_valid_name(prompt):
    """
    Ask for a name and keep asking until the user types something.
    Returns the name as a string.
    """
    while True:
        name = input(prompt).strip()
        if name == "":
            print("  Error: name cannot be empty. Please try again.")
        else:
            return name


def get_valid_int(prompt, lowest, highest):
    """
    Ask for a whole number between lowest and highest.
    Keeps asking if the user types something invalid.
    Returns the number as an integer.
    """
    while True:
        try:
            number = int(input(prompt))
            if number < lowest or number > highest:
                print(f"  Error: please enter a number between {lowest} and {highest}.")
            else:
                return number
        except ValueError:
            print("  Error: that is not a valid number. Please try again.")


def get_valid_score(prompt):
    """
    Ask for a score and keep asking until the user gives a
    number between 0 and 100.
    Returns the score as a float.
    """
    while True:
        try:
            score = float(input(prompt))
            if score < 0 or score > 100:
                print("  Error: score must be between 0 and 100.")
            else:
                return round(score, 2)
        except ValueError:
            print("  Error: please enter a number (e.g. 67.5).")


# ============================================================
# DISPLAY FUNCTIONS - printing results to the screen
# (these functions do NOT do any calculations)
# ============================================================

def print_student_report(student):
    """
    Print a full academic report for one student.
    Calls the calculation functions to get grade and risk,
    then displays everything neatly.
    """
    scores = student.get_scores()
    average = compute_average(scores)
    grade, grade_desc = get_grade(average)
    risk = get_risk_level(average, student.attendance)

    print("\n" + "=" * 50)
    print(f"  STUDENT REPORT - {student.student_id}")
    print("=" * 50)
    print(f"  Name       : {student.name}")
    print(f"  Attendance : {student.attendance}%")
    print()

    # Print each unit and its score
    print(f"  {'Unit':<25} {'Score':>6}")
    print("  " + "-" * 33)
    for unit in student.units:
        print(f"  {unit['unit_name']:<25} {unit['score']:>6.1f}")
    print("  " + "-" * 33)
    print(f"  {'Average':<25} {average:>6.1f}")
    print()
    print(f"  Grade       : {grade} - {grade_desc}")
    print(f"  Risk Level  : {risk}")

    # Give a short advisory message based on risk
    if risk == "High":
        print("\n  *** This student needs urgent academic support! ***")
    elif risk == "Moderate":
        print("\n  *  This student should be monitored carefully.")
    else:
        print("\n  *  This student is performing well.")

    print("=" * 50)


def print_all_students(students):
    """
    Print a summary table showing all registered students.
    Shows ID, name, average score, grade and risk level.
    """
    print("\n" + "=" * 50)
    print("  ALL STUDENTS")
    print("=" * 50)

    if len(students) == 0:
        print("  No students registered yet.")
        return

    # Print the table header
    print(f"  {'ID':<14} {'Name':<20} {'Avg':>5}  {'Grade':>5}  Risk")
    print("  " + "-" * 52)

    for student_id in students:
        student = students[student_id]
        average = compute_average(student.get_scores())
        grade, _ = get_grade(average)
        risk = get_risk_level(average, student.attendance)
        print(f"  {student_id:<14} {student.name:<20} {average:>5.1f}  {grade:>5}  {risk}")

    print(f"\n  Total: {len(students)} student(s)")


# ============================================================
# MENU ACTION FUNCTIONS - one function per menu option
# ============================================================

def register_student(students):
    """
    Ask for student details and add them to the system.
    Checks for a duplicate ID before registering.
    """
    print("\n--- Register New Student ---")

    # Get and validate the student ID
    student_id = get_valid_name("  Enter student ID: ").upper()

    if student_id in students:
        print(f"  Error: ID '{student_id}' is already registered.")
        return

    name = get_valid_name("  Enter full name: ")
    num_units = get_valid_int("  How many units is this student taking? (1-8): ", 1, 8)

    # Collect unit names and scores
    units = []
    for i in range(num_units):
        print(f"\n  Unit {i + 1} of {num_units}:")
        unit_name = get_valid_name("    Unit name: ")
        score = get_valid_score(f"    Score for {unit_name}: ")
        units.append({"unit_name": unit_name, "score": score})

    attendance = get_valid_score("  Attendance percentage (0-100): ")

    # Create the Student object and save it
    new_student = Student(student_id, name, units, attendance)
    students[student_id] = new_student
    save_students(students)

    print(f"\n  Student '{name}' registered successfully!")


def view_student(students):
    """
    Ask for a student ID and display their full report.
    Shows an error if the ID is not found.
    """
    print("\n--- View Student Report ---")

    student_id = get_valid_name("  Enter student ID: ").upper()

    if student_id not in students:
        print(f"  Error: no student found with ID '{student_id}'.")
        return

    print_student_report(students[student_id])


def update_student(students):
    """
    Update either the attendance or a unit score for a student.
    Saves the changes to the file after updating.
    """
    print("\n--- Update Student Record ---")

    student_id = get_valid_name("  Enter student ID: ").upper()

    if student_id not in students:
        print(f"  Error: no student found with ID '{student_id}'.")
        return

    student = students[student_id]
    print(f"\n  Updating record for: {student.name}")
    print("  1. Update attendance")
    print("  2. Update a unit score")

    choice = get_valid_int("  Choose (1 or 2): ", 1, 2)

    if choice == 1:
        student.attendance = get_valid_score("  New attendance percentage: ")
        print("  Attendance updated!")

    else:
        # Show the units so the user can pick one
        for i in range(len(student.units)):
            print(f"  {i + 1}. {student.units[i]['unit_name']}  (score: {student.units[i]['score']})")

        unit_choice = get_valid_int("  Which unit to update? ", 1, len(student.units))
        unit = student.units[unit_choice - 1]
        unit["score"] = get_valid_score(f"  New score for {unit['unit_name']}: ")
        print("  Score updated!")

    save_students(students)


def delete_student(students):
    """
    Remove a student record after asking for confirmation.
    The user must type 'yes' to confirm the deletion.
    """
    print("\n--- Delete Student Record ---")

    student_id = get_valid_name("  Enter student ID: ").upper()

    if student_id not in students:
        print(f"  Error: no student found with ID '{student_id}'.")
        return

    student = students[student_id]
    confirm = input(f"  Are you sure you want to delete '{student.name}'? (yes/no): ").strip().lower()

    if confirm == "yes":
        del students[student_id]
        save_students(students)
        print(f"  '{student.name}' has been deleted.")
    else:
        print("  Deletion cancelled.")


def show_at_risk_students(students):
    """
    Show a report of all students who are at Moderate or High risk.
    Uses get_risk_level() to check each student.
    """
    print("\n--- At-Risk Students ---")

    if len(students) == 0:
        print("  No students registered yet.")
        return

    # Go through every student and find the at-risk ones
    at_risk_list = []
    for student_id in students:
        student = students[student_id]
        average = compute_average(student.get_scores())
        risk = get_risk_level(average, student.attendance)
        if risk == "Moderate" or risk == "High":
            at_risk_list.append((student_id, student, average, risk))

    if len(at_risk_list) == 0:
        print("  No at-risk students found. All students are doing well!")
        return

    print(f"\n  {'ID':<14} {'Name':<20} {'Avg':>5}  Risk")
    print("  " + "-" * 46)
    for student_id, student, average, risk in at_risk_list:
        print(f"  {student_id:<14} {student.name:<20} {average:>5.1f}  {risk}")

    print(f"\n  {len(at_risk_list)} student(s) need attention.")


def show_class_statistics(students):
    """
    Show general statistics for the whole class:
    total students, class average, best and lowest performer.
    """
    print("\n--- Class Statistics ---")

    if len(students) == 0:
        print("  No students registered yet.")
        return

    # Collect all averages
    all_averages = {}
    for student_id in students:
        student = students[student_id]
        all_averages[student_id] = compute_average(student.get_scores())

    # Calculate class average
    total = 0
    for avg in all_averages.values():
        total = total + avg
    class_avg = round(total / len(all_averages), 2)

    # Find best and lowest
    best_id = max(all_averages, key=all_averages.get)
    lowest_id = min(all_averages, key=all_averages.get)

    # Count risk levels
    low_count = 0
    moderate_count = 0
    high_count = 0

    for student_id in students:
        student = students[student_id]
        risk = get_risk_level(all_averages[student_id], student.attendance)
        if risk == "Low":
            low_count = low_count + 1
        elif risk == "Moderate":
            moderate_count = moderate_count + 1
        else:
            high_count = high_count + 1

    print(f"\n  Total students  : {len(students)}")
    print(f"  Class average   : {class_avg}")
    print(f"  Best performer  : {students[best_id].name} ({best_id}) - {all_averages[best_id]}")
    print(f"  Lowest scorer   : {students[lowest_id].name} ({lowest_id}) - {all_averages[lowest_id]}")
    print()
    print(f"  Low risk        : {low_count} student(s)")
    print(f"  Moderate risk   : {moderate_count} student(s)")
    print(f"  High risk       : {high_count} student(s)")


# ============================================================
# SECTION F – EXTENSION FEATURE
# Scholarship Eligibility Checker
# ============================================================

def check_scholarship_eligibility(students):
    """
    Check which students are eligible for a scholarship.

    A student qualifies if they meet ALL three criteria:
        - Average score of 65 or above (Upper Second class or better)
        - Attendance percentage of 75 or above
        - Academic risk level is Low

    This feature is relevant to the Kenyan university context because
    scholarships and bursaries can be the difference between a student
    continuing their studies or dropping out due to financial pressure.
    """
    print("\n--- Scholarship Eligibility Report ---")

    if len(students) == 0:
        print("  No students registered yet.")
        return

    # Go through every student and check the three criteria
    eligible = []
    for student_id in students:
        student = students[student_id]
        average = compute_average(student.get_scores())
        risk = get_risk_level(average, student.attendance)

        # Student must meet all three conditions to qualify
        if average >= 65 and student.attendance >= 75 and risk == "Low":
            eligible.append((student_id, student.name, average, student.attendance))

    if len(eligible) == 0:
        print("  No students currently meet the scholarship criteria.")
        print("  Criteria: Average >= 65, Attendance >= 75%, Risk = Low")
        return

    print(f"\n  {'ID':<16} {'Name':<24} {'Average':>8}  {'Attendance':>10}")
    print("  " + "-" * 62)
    for student_id, name, average, attendance in eligible:
        print(f"  {student_id:<16} {name:<24} {average:>8.1f}  {attendance:>9.1f}%")

    print(f"\n  {len(eligible)} student(s) are eligible for a scholarship.")


# ============================================================
# MAIN PROGRAM - the menu loop
# ============================================================

def show_menu():
    """Print the main menu options to the screen."""
    print("""
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
    """)


def main():
    """
    The main function that runs the program.
    Loads students from the file, shows the menu,
    and calls the right function based on the user's choice.
    """
    # Load any saved student records when the program starts
    students = load_students()

    print("\n  Welcome to SAMSS!")
    print("  Student Academic Monitoring and Support System")

    # Keep showing the menu until the user chooses to exit
    while True:
        show_menu()
        choice = get_valid_int("  Enter your choice: ", 0, 8)

        if choice == 0:
            print("\n  Goodbye!\n")
            break
        elif choice == 1:
            register_student(students)
        elif choice == 2:
            view_student(students)
        elif choice == 3:
            print_all_students(students)
        elif choice == 4:
            update_student(students)
        elif choice == 5:
            delete_student(students)
        elif choice == 6:
            show_at_risk_students(students)
        elif choice == 7:
            show_class_statistics(students)
        elif choice == 8:
            check_scholarship_eligibility(students)

        input("\n  Press Enter to continue...")


# Run the program
main()
