from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'university.db'

# Create tables if not exists
def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS universities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT,
            founded_year INTEGER,
            total_students INTEGER,
            faculty_members INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            university_id INTEGER,
            program_name TEXT,
            department TEXT,
            duration INTEGER,
            degrees_offered TEXT,
            FOREIGN KEY (university_id) REFERENCES universities (id)
        )
    ''')

    conn.commit()
    conn.close()

# Initialize tables
create_tables()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Fetch data from universities and courses tables
    cursor.execute('SELECT * FROM universities')
    universities = cursor.fetchall()

    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()

    conn.close()

    return render_template('index.html', universities=universities, courses=courses)

@app.route('/add_university', methods=['POST'])
def add_university():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        founded_year = request.form['founded_year']
        total_students = request.form['total_students']
        faculty_members = request.form['faculty_members']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Insert data into universities table
        cursor.execute('''
            INSERT INTO universities (name, location, founded_year, total_students, faculty_members)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, location, founded_year, total_students, faculty_members))

        conn.commit()
        conn.close()

    return redirect(url_for('index'))

@app.route('/add_course', methods=['POST'])
def add_course():
    if request.method == 'POST':
        university_id = request.form['university_id']
        program_name = request.form['program_name']
        department = request.form['department']
        duration = request.form['duration']
        degrees_offered = request.form['degrees_offered']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Insert data into courses table
        cursor.execute('''
            INSERT INTO courses (university_id, program_name, department, duration, degrees_offered)
            VALUES (?, ?, ?, ?, ?)
        ''', (university_id, program_name, department, duration, degrees_offered))

        conn.commit()
        conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
