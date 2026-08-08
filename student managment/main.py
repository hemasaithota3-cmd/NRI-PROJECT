# Student Management System Using a Dictionary

students = {}


# Add a new student
def add_student():
    student_id = input("Enter Student ID: ")

    if student_id in students:
        print("Student ID already exists!")
        return

    name = input("Enter Student Name: ")
    age = int(input("Enter Age: "))
    course = input("Enter Course: ")
    marks = float(input("Enter Marks: "))

    students[student_id] = {
        "name": name,
        "age": age,
        "course": course,
        "marks": marks
    }

    print("Student added successfully!")


# Display all students
def display_students():
    if not students:
        print("No student records found.")
        return

    print("\n========== STUDENT RECORDS ==========")

    for student_id, details in students.items():
        print(f"\nStudent ID : {student_id}")
        print(f"Name       : {details['name']}")
        print(f"Age        : {details['age']}")
        print(f"Course     : {details['course']}")
        print(f"Marks      : {details['marks']}")


# Search for a student
def search_student():
    student_id = input("Enter Student ID to search: ")

    if student_id in students:
        details = students[student_id]

        print("\nStudent Found!")
        print(f"Student ID : {student_id}")
        print(f"Name       : {details['name']}")
        print(f"Age        : {details['age']}")
        print(f"Course     : {details['course']}")
        print(f"Marks      : {details['marks']}")
    else:
        print("Student not found.")


# Update student details
def update_student():
    student_id = input("Enter Student ID to update: ")

    if student_id not in students:
        print("Student not found.")
        return

    print("\nEnter new details:")

    name = input("Enter Name: ")
    age = int(input("Enter Age: "))
    course = input("Enter Course: ")
    marks = float(input("Enter Marks: "))

    students[student_id] = {
        "name": name,
        "age": age,
        "course": course,
        "marks": marks
    }

    print("Student details updated successfully!")


# Delete a student
def delete_student():
    student_id = input("Enter Student ID to delete: ")

    if student_id in students:
        del students[student_id]
        print("Student deleted successfully!")
    else:
        print("Student not found.")


# Main menu
def main():
    while True:
        print("\n====================================")
        print("     STUDENT MANAGEMENT SYSTEM")
        print("====================================")
        print("1. Add Student")
        print("2. Display Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("====================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            display_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            update_student()

        elif choice == "5":
            delete_student()

        elif choice == "6":
            print("Thank you for using Student Management System!")
            break

        else:
            print("Invalid choice! Please try again.")


# Run the program
if __name__ == "__main__":
    main()