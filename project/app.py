from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import os
import db

app = Flask(__name__)
app.secret_key = 'some_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    courses = db.fetch_courses()
    students = db.fetch_students()
    enrollments = db.fetch_enrollments()
    assignments = db.fetch_assignments()
    submissions = db.fetch_submissions()
    return render_template('index.html', courses=courses, students=students, enrollments=enrollments, assignments=assignments, submissions=submissions)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        teacher = request.form['teacher']
        db.add_course(name, description, teacher)
        flash('Курс додано успішно!')
        return redirect(url_for('index'))
    return render_template('add_course.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        db.add_student(name)
        flash('Студента додано успішно!')
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    if request.method == 'POST':
        student_name = request.form['student_name']
        course_name = request.form['course_name']
        db.enroll_student(student_name, course_name)
        flash('Студента успішно зараховано на курс!')
        return redirect(url_for('index'))
    return render_template('enroll_student.html', students=db.fetch_students(), courses=db.fetch_courses())

@app.route('/add_assignment', methods=['GET', 'POST'])
def add_assignment():
    if request.method == 'POST':
        name = request.form['name']
        course_name = request.form['course_name']
        db.add_assignment(name, course_name)
        flash('Завдання додано успішно!')
        return redirect(url_for('index'))
    return render_template('add_assignment.html', courses=db.fetch_courses())

@app.route('/submit_assignment', methods=['GET', 'POST'])
def submit_assignment():
    if request.method == 'POST':
        assignment_name = request.form['assignment_name']
        student_name = request.form['student_name']
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            db.submit_assignment(assignment_name, student_name, filename)
            flash('Завдання успішно здано!')
            return redirect(url_for('index'))
    return render_template('submit_assignment.html', assignments=db.fetch_assignments(), students=db.fetch_students())

@app.route('/grade_submission', methods=['GET', 'POST'])
def grade_submission():
    if request.method == 'POST':
        submission_id = request.form['submission_id']
        grade = request.form['grade']
        db.grade_submission(submission_id, grade)
        flash('Оцінку встановлено успішно!')
        return redirect(url_for('index'))
    return render_template('grade_submission.html', submissions=db.fetch_submissions())

@app.route('/view_courses')
def view_courses():
    courses = db.fetch_courses()
    return render_template('view_courses.html', courses=courses)

@app.route('/view_students')
def view_students():
    students = db.fetch_students()
    return render_template('view_students.html', students=students)

@app.route('/view_assignments')
def view_assignments():
    assignments = db.fetch_assignments()
    return render_template('view_assignments.html', assignments=assignments)

@app.route('/view_enrollments')
def view_enrollments():
    enrollments = db.fetch_enrollments()
    return render_template('view_enrollments.html', enrollments=enrollments)

@app.route('/view_submissions', methods=['GET', 'POST'])
def view_submissions():
    if request.method == 'POST':
        submission_id = request.form['submission_id']
        grade = request.form['grade']
        db.grade_submission(submission_id, grade)
        flash('Оцінку успішно виставлено!')
        return redirect(url_for('view_submissions'))
    submissions = db.fetch_submissions()
    print(f'Submissions passed to template: {submissions}')  # Debug line
    return render_template('view_submissions.html', submissions=submissions)


if __name__ == '__main__':
    db.create_tables()
    app.run(debug=True)
