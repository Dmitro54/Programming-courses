import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            teacher TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY,
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students (id),
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY,
            assignment_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            file_name TEXT NOT NULL,
            grade INTEGER DEFAULT 0,
            FOREIGN KEY (assignment_id) REFERENCES assignments (id),
            FOREIGN KEY (student_id) REFERENCES students (id)
        )
    ''')
    conn.commit()
    conn.close()

def fetch_courses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    return courses

def fetch_students():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students

def fetch_enrollments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT enrollments.id, students.name, courses.name FROM enrollments
        JOIN students ON enrollments.student_id = students.id
        JOIN courses ON enrollments.course_id = courses.id
    ''')
    enrollments = cursor.fetchall()
    conn.close()
    return enrollments

def fetch_assignments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assignments')
    assignments = cursor.fetchall()
    conn.close()
    return assignments

def fetch_submissions():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT submissions.id, assignments.name, students.name, submissions.grade, submissions.file_name FROM submissions
        JOIN assignments ON submissions.assignment_id = assignments.id
        JOIN students ON submissions.student_id = students.id
    ''')
    submissions = cursor.fetchall()
    conn.close()
    return submissions

def add_course(name, description, teacher):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO courses (name, description, teacher) VALUES (?, ?, ?)', (name, description, teacher))
    conn.commit()
    conn.close()

def add_student(name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

def enroll_student(student_name, course_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM students WHERE name = ?', (student_name,))
    student_id = cursor.fetchone()
    if student_id is None:
        raise ValueError(f"Student with name '{student_name}' not found.")
    student_id = student_id[0]
    
    cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
    course_id = cursor.fetchone()
    if course_id is None:
        raise ValueError(f"Course with name '{course_name}' not found.")
    course_id = course_id[0]

    cursor.execute('INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
    conn.commit()
    conn.close()

def add_assignment(name, course_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM courses WHERE name = ?', (course_name,))
    course_id = cursor.fetchone()
    if course_id is None:
        raise ValueError(f"Course with name '{course_name}' not found.")
    course_id = course_id[0]
    
    cursor.execute('INSERT INTO assignments (name, course_id) VALUES (?, ?)', (name, course_id))
    conn.commit()
    conn.close()

def submit_assignment(assignment_name, student_name, file_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM assignments WHERE name = ?', (assignment_name,))
    assignment_id = cursor.fetchone()
    if assignment_id is None:
        raise ValueError(f"Assignment with name '{assignment_name}' not found.")
    assignment_id = assignment_id[0]

    cursor.execute('SELECT id FROM students WHERE name = ?', (student_name,))
    student_id = cursor.fetchone()
    if student_id is None:
        raise ValueError(f"Student with name '{student_name}' not found.")
    student_id = student_id[0]

    cursor.execute('INSERT INTO submissions (assignment_id, student_id, file_name, grade) VALUES (?, ?, ?, 0)', (assignment_id, student_id, file_name))
    conn.commit()
    conn.close()

def grade_submission(submission_id, grade):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE submissions SET grade = ? WHERE id = ?', (grade, submission_id))
    conn.commit()
    conn.close()

def alter_submissions_table():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('PRAGMA table_info(submissions)')
    columns = cursor.fetchall()
    if not any(column[1] == 'grade' for column in columns):
        cursor.execute('ALTER TABLE submissions ADD COLUMN grade INTEGER DEFAULT 0')
    conn.commit()
    conn.close()
