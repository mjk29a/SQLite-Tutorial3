import sqlite3

conn = sqlite3.connect("students.db")
conn.execute("PRAGMA foreign_keys = ON;")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS registered_courses (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS grades (
    student_id INT,
    course_id INT,
    grade REAL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

cursor.execute("DELETE FROM grades")
cursor.execute("DELETE FROM registered_courses")
cursor.execute("DELETE FROM student")

students = [
    (1, "Alice", 20),
    (2, "Bob", 22),
    (3, "Charlie", 21)
]
cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)

registered = [
    (1, 101),
    (1, 102),
    (2, 101),
    (3, 103)
]
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered)

grades_data = [
    (1, 101, 85),
    (1, 102, 92),
    (2, 101, 78),
    (3, 103, 88)
]
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades_data)

conn.commit()

cursor.execute("""
SELECT g.student_id, g.course_id, g.grade
FROM grades g
JOIN (
    SELECT student_id, MAX(grade) AS max_grade
    FROM grades
    GROUP BY student_id
) mx
ON g.student_id = mx.student_id AND g.grade = mx.max_grade
ORDER BY g.student_id
""")

print("Max grade per student:")
for row in cursor.fetchall():
    print(row)

student_id = 1
cursor.execute("SELECT AVG(grade) FROM grades WHERE student_id = ?", (student_id,))
print("Average grade of student 1:", cursor.fetchone()[0])

conn.close()
