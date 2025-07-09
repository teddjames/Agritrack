from flask import Flask, render_template, request, redirect
import sqlite3
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.secret_key = '482716'  

DB_PATH = 'data/agritrack.db'

# --- DATABASE SETUP ---
def init_db():
    if not os.path.exists(DB_PATH):
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Create tables
        c.execute('''CREATE TABLE expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT,
                        item TEXT,
                        amount REAL,
                        date TEXT)''')

        c.execute('''CREATE TABLE tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task TEXT,
                        date TEXT,
                        status TEXT)''')

        c.execute('''CREATE TABLE sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item TEXT,
                        quantity REAL,
                        price REAL,
                        buyer TEXT,
                        date TEXT)''')

        # ✅ Add this if it's not already there
        c.execute('''CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

        conn.commit()
        conn.close()

# --- HOME/DASHBOARD ---
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')  # 🔐 redirect if not logged in

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM expenses")
    total_expenses = c.fetchone()[0] or 0

    c.execute("SELECT SUM(quantity * price) FROM sales")
    total_sales = c.fetchone()[0] or 0

    c.execute("SELECT task, date FROM tasks WHERE status='pending'")
    upcoming_tasks = c.fetchall()

    conn.close()
    return render_template("index.html", expenses=total_expenses, sales=total_sales, tasks=upcoming_tasks, now=datetime.now())

# --- EXPENSES ---
@app.route('/expenses', methods=['GET', 'POST'])
def expenses():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        category = request.form['category']
        item = request.form['item']
        amount = float(request.form['amount'])
        date = request.form['date']
        c.execute("INSERT INTO expenses (category, item, amount, date) VALUES (?, ?, ?, ?)",
                  (category, item, amount, date))
        conn.commit()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return render_template("expenses.html", expenses=rows)

# --- TASKS ---
@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        task = request.form['task']
        date = request.form['date']
        c.execute("INSERT INTO tasks (task, date, status) VALUES (?, ?, ?)",
                  (task, date, 'pending'))
        conn.commit()
    c.execute("SELECT * FROM tasks ORDER BY date ASC")
    tasks = c.fetchall()
    conn.close()
    return render_template("tasks.html", tasks=tasks)

# --- MARK TASK AS DONE ---
@app.route('/tasks/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/tasks')

# --- SALES ---
@app.route('/sales', methods=['GET', 'POST'])
def sales():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        item = request.form['item']
        quantity = float(request.form['quantity'])
        price = float(request.form['price'])
        buyer = request.form['buyer']
        date = request.form['date']
        c.execute("INSERT INTO sales (item, quantity, price, buyer, date) VALUES (?, ?, ?, ?, ?)",
                  (item, quantity, price, buyer, date))
        conn.commit()
    c.execute("SELECT * FROM sales ORDER BY date DESC")
    sales = c.fetchall()
    conn.close()
    return render_template("sales.html", sales=sales)

# ---SIGN UP---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username already exists.')
            return redirect('/signup')
        conn.close()
        flash('Account created. Please log in.')
        return redirect('/login')
    return render_template('signup.html')

#--- LOGIN ----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/')
        else:
            flash('Invalid login.')
            return redirect('/login')
    return render_template('login.html')

#---LOG OUT---
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.')
    return redirect('/login')



if __name__ == '__main__':
    init_db()
    app.run(debug=True)
