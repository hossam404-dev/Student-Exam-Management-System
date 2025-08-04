from logs import student_exists
def login_admin():
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    return username == "admin" and password == "1234"

def login_student():
    name = input("Enter your full name: ").strip()
    student_id = input("Enter your student ID: ").strip()
    if student_exists(name, student_id):
        return {"name": name, "id": student_id}
    return None
