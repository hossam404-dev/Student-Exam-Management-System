import os
import numpy as np

BASE_PATH = r"WRITE YOUR DIRECTORY HERE"
QUESTIONS_FILE = os.path.join(BASE_PATH, "questions.txt") # DON'T FORGET TO CREATE THOSE NEXT 3 TXT FILES EACH OF THEM AND MAINTAIN THEIR FUNCTIONALITY
ANSWERS_FILE = os.path.join(BASE_PATH, "answers.txt")
REPORT_FILE = os.path.join(BASE_PATH, "report.txt")
STUDENTS_DIR = "students"

class Exam:
    def __init__(self):
        self.questions = self.show_questions()
        self.answer_key = self.show_answers()

    def show_questions(self):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print("Questions file not found.")
            return []

    def show_answers(self):
        try:
            with open(ANSWERS_FILE, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print("Answers file not found.")
            return []

    def store_questions(self):
        with open(QUESTIONS_FILE, "w", encoding="utf-8") as f:
            for question in self.questions:
                f.write(question + "\n")

    def store_answers(self):
        with open(ANSWERS_FILE, "w", encoding="utf-8") as f:
            for ans in self.answer_key:
                f.write(ans + "\n")

    def grade(self, student_answers):
        correct = 0
        detailed = []

        for i, (student_ans, correct_ans) in enumerate(zip(student_answers, self.answer_key)):
            if student_ans == correct_ans:
                correct += 1
                mark = "Correct"  
            elif student_ans == "":
                mark = "Empty"
            else:
                mark = "Wrong"  

            detailed.append((i + 1, student_ans, correct_ans, mark))

        return correct, detailed


    def generate_detailed_report(self, name, student_id, score, detailed):
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(f"\n--- Report for {name} (ID: {student_id}) ---\n")
            for qn, ans, correct, mark in detailed:
                f.write(f"Q{qn}: Your Answer: {ans} | Correct Answer: {correct} | Result: {mark}\n")
            f.write(f"Score: {score}/{len(self.answer_key)}\n")
            f.write("Passed\n" if score >= len(self.answer_key) / 2 else "Failed\n")
            f.write("-" * 40 + "\n")

    def get_all_scores(self):
        scores = []
        if not os.path.exists(STUDENTS_DIR):
            print("No student data found.")
            return scores

        for student_folder in os.listdir(STUDENTS_DIR):
            answers_file = os.path.join(STUDENTS_DIR, student_folder, "answers.txt")
            if os.path.exists(answers_file):
                with open(answers_file, "r", encoding="utf-8") as f:
                    answers = [line.strip() for line in f if line.strip()]
                correct, _ = self.grade(answers)
                scores.append((student_folder, correct))

        def get_score(item):
            return item[1]

        scores.sort(key=get_score, reverse=True)

        return scores


    def print_scoreboard(self):
        scores = self.get_all_scores()
        print("\n--- Scoreboard ---")
        if not scores:
            print("No scores available.")
            return
        for name, score in scores:
            status = "Passed" if score >= len(self.answer_key) / 2 else "Failed"
            print(f"{name}: {score}/{len(self.answer_key)} - {status}")

    def show_statistics(self):
        scores = [score for _, score in self.get_all_scores()]
        if scores:
            print("\n--- Statistics ---")
            print(f"Max Score       : {max(scores)}")
            print(f"Min Score       : {min(scores)}")
            print(f"Average Score   : {np.mean(scores):.2f}")
            print(f"Median Score    : {np.median(scores):.2f}")
        else:
            print("No data available.")

    def view_student_report(self, student_name):
        """Allow admin to view a specific student's report directly."""
        answers_file = os.path.join(STUDENTS_DIR, student_name, "answers.txt")
        if not os.path.exists(answers_file):
            print("Student not found.")
            return

        with open(answers_file, "r", encoding="utf-8") as f:
            answers = [line.strip() for line in f.readlines()]
        score, detailed = self.grade(answers)
        print(f"\n--- Report for {student_name} ---")
        for qn, ans, correct, mark in detailed:
            print(f"Q{qn}: Your Answer: {ans} | Correct Answer: {correct} | Result: {mark}")
        print(f"Score: {score}/{len(self.answer_key)}")
        print("Passed\n" if score >= len(self.answer_key) / 2 else "Failed")

    def edit_answer_key(self):
        print("\n--- Current Answer Key ---")
        for i, ans in enumerate(self.answer_key, start=1):
            print(f"{i}. {ans}")
        try:
            qn = int(input("Enter question number to edit answer: "))
            if 1 <= qn <= len(self.answer_key):
                new_ans = input("Enter new correct answer: ").strip()
                self.answer_key[qn - 1] = new_ans
                self.store_answers()
                print("Answer key updated.")
            else:
                print("Invalid question number.")
        except ValueError:
            print("Invalid input.")

