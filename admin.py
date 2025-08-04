from exam import Exam
from logs import log_action

class Admin:
    def __init__(self):
        self.exam = Exam()

    def menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. View Questions")
            print("2. Edit Question")
            print("3. View Scoreboard")
            print("4. View Statistics")
            print("5. Add Question")
            print("6. Delete Question")
            print("7. Edit Answer Key")
            print("8. View Student Report")
            print("9. Logout")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.view_questions()
            elif choice == "2":
                self.edit_question()
            elif choice == "3":
                self.exam.print_scoreboard()
            elif choice == "4":
                self.exam.show_statistics()
            elif choice == "5":
                self.add_question()
            elif choice == "6":
                self.delete_question()
            elif choice == "7":
                self.exam.edit_answer_key()
                log_action("Admin edited the answer key")
            elif choice == "8":
                self.view_student_report()
            elif choice == "9":
                log_action("Admin logged out")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_questions(self):
        print("\n--- Questions ---")
        if not self.exam.questions:
            print("No questions available.")
            return
        for i, q in enumerate(self.exam.questions, start=1):
            print(f"Q{i}: {q}")

    def edit_question(self):
        self.view_questions()
        try:
            q_num = int(input("Enter question number to edit: "))
            if 1 <= q_num <= len(self.exam.questions):
                new_q = input("Enter new question: ").strip()
                self.exam.questions[q_num - 1] = new_q
                self.exam.store_questions()
                print("Question updated.")
                log_action(f"Admin edited question #{q_num}")
            else:
                print("Invalid question number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def add_question(self):
        question = input("Enter new question: ").strip()
        if question:
            self.exam.questions.append(question)
            self.exam.store_questions()
            print("Question added.")
            log_action("Admin added a new question")
        else:
            print("Question cannot be empty.")

    def delete_question(self):
        self.view_questions()
        try:
            q_num = int(input("Enter question number to delete: "))
            if 1 <= q_num <= len(self.exam.questions):
                deleted_q = self.exam.questions.pop(q_num - 1)
                self.exam.store_questions()
                print("Question deleted.")
                log_action(f"Admin deleted question #{q_num}: {deleted_q}")
            else:
                print("Invalid question number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def view_student_report(self):
        student_name = input("Enter the student folder name: ").strip().replace(" ","_")
        if student_name:
            self.exam.view_student_report(student_name)
            log_action(f"Admin viewed report for {student_name}")
        else:
            print("Student name cannot be empty.")
