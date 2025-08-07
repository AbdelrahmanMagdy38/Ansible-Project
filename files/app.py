from flask import Flask, request, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'notes.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO notes (content, timestamp) VALUES (?, ?)', (content, timestamp))
        conn.commit()
        conn.close()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT content, timestamp FROM notes ORDER BY id DESC')
    notes = cursor.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=80)

