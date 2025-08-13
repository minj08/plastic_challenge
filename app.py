from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import sqlite3
from model import classify_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 이미지 제공
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 초기 DB 설정
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        points INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS record (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        filename TEXT,
        recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# 홈 화면
@app.route('/')
def home():
    return render_template('home.html')

# 기록 화면
@app.route('/record')
def record():
    return render_template('record.html')

# 통계 화면
@app.route('/stats')
def stats():
    return render_template('stats.html')

# 사용자 생성
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

# 이미지 업로드
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
    c.execute("INSERT INTO record (user_id, action, filename) VALUES (?, ?, ?)", (user_id, action, filename))
    conn.commit()
    conn.close()

    return jsonify({'result': label, 'grams': grams, 'points': points})

# 사용자 정보 조회
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT username, points FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return jsonify({'username': user[0], 'points': user[1]})

# 이미지 갤러리
@app.route('/gallery')
def gallery():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT filename FROM record ORDER BY recorded_at DESC")
    images = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('gallery.html', images=images)

# 통계 데이터 API
@app.route('/user_stats')
def user_stats():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("""
        SELECT date(recorded_at), SUM(points * 5)
        FROM record
        GROUP BY date(recorded_at)
    """)
    rows = c.fetchall()
    conn.close()
    labels = [row[0] for row in rows]
    values = [row[1] for row in rows]
    return jsonify({'labels': labels, 'values': values})

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=5050)
