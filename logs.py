import os
import datetime

LOG_FILE = r"C:\Users\PCCV\Desktop\python_nti\Student-Exam Management Project\data\logs.txt"
STUDENT_FILE = r"C:\Users\PCCV\Desktop\python_nti\Student-Exam Management Project\data\students.txt"
STUDENT_FOLDER = "students"

def log_action(action):
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time_str}] {action}\n")

def student_exists(name, student_id):
    if not os.path.exists(STUDENT_FILE):
        return False
    name = name.strip().lower()
    student_id = student_id.strip()
    with open(STUDENT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 2:
                continue
            full_name, sid = parts
            if full_name.strip().lower() == name and sid.strip() == student_id:
                return True
    return False

def ensure_student_folder(name, student_id):
    folder_name = f"{name.replace(' ', '_')}_{student_id}"
    path = os.path.join(STUDENT_FOLDER, folder_name)
    os.makedirs(path, exist_ok=True)
    return path
