from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'payal_saini_secret'

# Database create
def init_db():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT, email TEXT UNIQUE, password TEXT, phone TEXT, course TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        course = request.form['course']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO students (name,email,password,phone,course) VALUES (?,?,?,?,?)",
                      (name,email,password,phone,course))
            conn.commit()
        except:
            pass
        conn.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE email=? AND password=?", (email, password))
        student = c.fetchone()
        conn.close()
        if student:
            session['student'] = student
            return render_template('dashboard.html', student=student)
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'student' in session:
        return render_template('dashboard.html', student=session['student'])
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('student', None)
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)