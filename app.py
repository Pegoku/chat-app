# pip freeze > requirements.txt

from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY, username TEXT, message TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

# Insert a message into the database
def insert_message(username, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    timestamp = datetime.datetime.now().strftime("%H:%M %d-%m-%Y")
    c.execute("INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
              (username, message, timestamp))
    conn.commit()
    conn.close()

# Retrieve messages from the database
def get_messages():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT username, message, timestamp FROM messages ORDER BY id")
    messages = c.fetchall()
    conn.close()
    return messages

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    insert_message(data['username'], data['message'])
    return jsonify({'status': 'success'})

@app.route('/messages', methods=['GET'])
def fetch_messages():
    messages = get_messages()
    return jsonify({'messages': messages})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)