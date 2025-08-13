# app.py
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import sqlite3
from model import classify_image

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        points INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/create_user', methods=['POST'])
def create_user():
    username = request.form['username']
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username) VALUES (?)", (username,))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return jsonify({'user_id': user_id})

@app.route('/upload', methods=['POST'])
def upload():
    user_id = request.form['user_id']
    action = request.form['action']
    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    label = classify_image(filepath)
    grams = 10 if label == "plastic" else 0
    points = round(grams / 5)

    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE users SET points = points + ? WHERE id = ?", (points, user_id))
    conn.commit()
    conn.close()

    return jsonify({'result': label, 'grams': grams, 'points': points})

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return jsonify({'username': user[0], 'points': user[1]})

@app.route('/')
def home():
    return '''
    <h1>🌱 플라스틱 제로 챌린지</h1>
    <p>API 서버가 정상적으로 실행 중입니다.</p>
    <ul>
        <li><a href="/user/1">사용자 정보 보기</a></li>
        <li>POST /create_user</li>
        <li>POST /upload</li>
    </ul>
    '''

if __name__ == '__main__':
    app.run(debug=True)