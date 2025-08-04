import os
import time
import random
from exam import Exam
from logs import log_action, ensure_student_folder

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.folder_path = ensure_student_folder(name, student_id)
        self.exam = Exam()

    def take_exam(self):
        answer_path = os.path.join(self.folder_path, "answers.txt")

        if os.path.exists(answer_path):
            print("\nYou have already taken the exam.")
            confirm = input("Do you want to retake it and overwrite previous answers? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("Exam cancelled.")
                return

        num_questions = len(self.exam.questions)
        print(f"\nExam Started. You have 10 minutes to answer {num_questions} questions.\n")
        start_time = time.time()
        max_duration = 600

        questions_with_index = list(enumerate(self.exam.questions))
        random.shuffle(questions_with_index)

        student_answers = [""] * num_questions

        for count, (original_index, question) in enumerate(questions_with_index):
            elapsed = time.time() - start_time
            if elapsed >= max_duration:
                print("\nTime is up! Submitting your answers...")
                break

            remaining = int(max_duration - elapsed)
            print(f"Q{count+1}: {question}")
            print(f"Time remaining: {remaining // 60}:{remaining % 60:02d}")
            answer = input("Your answer: ").strip()
            while answer == "":
                answer = input("Answer cannot be empty. Please enter your answer: ").strip()

            student_answers[original_index] = answer
        for i in range(num_questions):
            if student_answers[i] == "":
                student_answers[i] = ""

        with open(answer_path, "w", encoding="utf-8") as f:
            for ans in student_answers:
                f.write(ans + "\n")

        score, detailed = self.exam.grade(student_answers)
        print(f"\nYour score: {score}/{num_questions}")
        status = "Passed" if score >= num_questions / 2 else "Failed"
        print(f"Status: {status}")

        self.exam.generate_detailed_report(self.name, self.student_id, score, detailed)
        log_action(f"Student {self.name} ({self.student_id}) submitted exam. Score: {score}")
