from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB = "database.db"

# Create DB table
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lost_found (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                contact TEXT,
                item TEXT,
                description TEXT,
                status TEXT DEFAULT 'Lost')''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        item = request.form['item']
        description = request.form['description']

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("INSERT INTO lost_found (name, contact, item, description) VALUES (?, ?, ?, ?)",
                  (name, contact, item, description))
        conn.commit()
        conn.close()

        return redirect('/view')
    return render_template('report.html')

@app.route('/view')
def view():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM lost_found")
    records = c.fetchall()
    conn.close()
    return render_template('view.html', records=records)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)