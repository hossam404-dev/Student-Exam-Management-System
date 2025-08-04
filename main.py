from login import login_admin, login_student
from admin import Admin
from student import Student
txt ="Exam Management System"
def main():
    
    print(txt.center(77,"="))

    while True:
        print("\nPlease select an option:")
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            if login_admin():
                admin = Admin()
                admin.menu()
            else:
                print("Invalid admin credentials.")
        elif choice == "2":
            student_info = login_student()
            if student_info:
                student = Student(student_info["name"], student_info["id"])
                student.take_exam()
            else:
                print("Student not found.")
        elif choice == "3":
            print("Exiting the system!")
            break
        else:
            print("Invalid choice. Please try again.")


main()
