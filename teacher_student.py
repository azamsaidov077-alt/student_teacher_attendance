import psycopg2
from datetime import datetime


conn = psycopg2.connect(
    host="localhost",
    database="attendance_db",
    user="postgres",
    password="1234"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE,
    kelgan TIMESTAMP,
    ketgan TIMESTAMP
)
""")
conn.commit()


default_students = ["Ali", "Laylo", "Jasur"]
for student in default_students:
    cursor.execute("INSERT INTO students (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (student,))
conn.commit()



def show_student_status(name):
    cursor.execute("SELECT kelgan, ketgan FROM students WHERE name = %s;", (name,))
    result = cursor.fetchone()
    if result:
        kelgan, ketgan = result
        print(f"\n👤 {name}ning yo‘qlamasi:")
        print(f"   Kelgan: {kelgan}")
        print(f"   Ketgan: {ketgan}\n")
    else:
        print(" Bunday o‘quvchi topilmadi.\n")


def teacher_panel():
    while True:
        print("\n O‘qituvchi paneli:")
        print("1. Barcha o‘quvchilarni ko‘rish")
        print("2. O‘quvchini kelgan deb belgilash")
        print("3. O‘quvchini ketgan deb belgilash")
        print("4. Chiqish")
        tanlov = input("Tanlovni kiriting: ")

        if tanlov == "1":
            cursor.execute("SELECT name, kelgan, ketgan FROM students ORDER BY id;")
            rows = cursor.fetchall()
            for row in rows:
                print(f"{row[0]}: kelgan={row[1]}, ketgan={row[2]}")
        elif tanlov == "2":
            name = input("O‘quvchi ismini kiriting: ")
            vaqt = datetime.now()
            cursor.execute("UPDATE students SET kelgan = %s WHERE name = %s;", (vaqt, name))
            conn.commit()
            print(f"{name} kelgan vaqt belgilang.")
        elif tanlov == "3":
            name = input("O‘quvchi ismini kiriting: ")
            vaqt = datetime.now()
            cursor.execute("UPDATE students SET ketgan = %s WHERE name = %s;", (vaqt, name))
            conn.commit()
            print(f"{name} ketgan vaqt belgilang.")
        elif tanlov == "4":
            break
        else:
            print("Noto‘g‘ri tanlov!\n")


def student_panel():
    name = input("Ismingizni kiriting: ")
    show_student_status(name)


def main():
    while True:
        print("\n Yo‘qlama tizimi (PostgreSQL bilan)")
        print("1. O‘qituvchi sifatida kirish")
        print("2. O‘quvchi sifatida kirish")
        print("3. Chiqish")
        tanlov = input("Tanlovni kiriting: ")

        if tanlov == "1":
            teacher_panel()
        elif tanlov == "2":
            student_panel()
        elif tanlov == "3":
            print("Tizimdan chiqildi.")
            break
        else:
            print("Noto‘g‘ri tanlov!\n")


if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()


