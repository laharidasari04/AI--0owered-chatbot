from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import json
import os
from datetime import datetime
from chatbot import Chatbot

app = Flask(__name__)
CORS(app)

# Initialize chatbot
chatbot = Chatbot()

# Database setup
def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_id = data.get('user_id', 'anonymous')
        
        if not user_message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get bot response
        bot_response = chatbot.get_response(user_message)
        
        # Log conversation to database
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (user_id, user_message, bot_response)
            VALUES (?, ?, ?)
        ''', (user_id, user_message, bot_response))
        conn.commit()
        conn.close()
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conversations', methods=['GET'])
def get_conversations():
    try:
        user_id = request.args.get('user_id', 'anonymous')
        limit = request.args.get('limit', 50)
        
        conn = sqlite3.connect('chatbot.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_message, bot_response, timestamp
            FROM conversations
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                'user_message': row[0],
                'bot_response': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return jsonify({'conversations': conversations})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 