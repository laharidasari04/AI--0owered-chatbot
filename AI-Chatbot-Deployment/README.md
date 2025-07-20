# AI-Powered Chatbot

An intelligent chatbot built with Python, Flask, and Natural Language Processing (NLP) for customer support and FAQs.

## Features

- 🤖 **Intelligent Responses**: Uses transformers and NLTK for natural language understanding
- 💬 **Real-time Chat**: Modern web interface with real-time messaging
- 📊 **Conversation Logging**: SQLite database to store and retrieve conversation history
- 🎯 **Intent Recognition**: Detects user intent (greetings, help, weather, etc.)
- 😊 **Sentiment Analysis**: Analyzes user sentiment for contextual responses
- 📱 **Responsive Design**: Beautiful, mobile-friendly UI
- 🔄 **Context Awareness**: Maintains conversation context and history

## Technologies Used

- **Backend**: Python, Flask, SQLite
- **NLP**: Transformers, NLTK
- **Frontend**: HTML, CSS, JavaScript
- **AI Models**: DistilBERT for sentiment analysis

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the chatbot**:
   Open your browser and go to `http://localhost:5000`

## Project Structure

```
AI-Powered-Chatbot/
├── app.py                 # Main Flask application
├── chatbot.py            # Core chatbot logic with NLP
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Web interface
├── chatbot.db           # SQLite database (created automatically)
└── README.md           # This file
```

## How It Works

### 1. Natural Language Processing
- **Intent Detection**: Recognizes user intent using keyword matching
- **Sentiment Analysis**: Uses DistilBERT model to analyze message sentiment
- **Text Preprocessing**: Cleans and normalizes input text

### 2. Response Generation
- **Contextual Responses**: Generates responses based on intent and sentiment
- **FAQ System**: Predefined responses for common queries
- **Dynamic Responses**: Intelligent responses for general conversations

### 3. Web Interface
- **Real-time Chat**: Instant message sending and receiving
- **Conversation History**: Loads previous conversations
- **Typing Indicators**: Shows when the bot is processing
- **Responsive Design**: Works on desktop and mobile

### 4. Data Storage
- **SQLite Database**: Stores all conversations with timestamps
- **User Sessions**: Tracks conversations by user ID
- **Analytics**: Conversation summaries and statistics

## API Endpoints

### POST `/api/chat`
Send a message to the chatbot.

**Request Body:**
```json
{
  "message": "Hello, how are you?",
  "user_id": "user_123"
}
```

**Response:**
```json
{
  "response": "Hello! How can I help you today?",
  "timestamp": "2024-01-15T10:30:00"
}
```

### GET `/api/conversations`
Retrieve conversation history.

**Query Parameters:**
- `user_id`: User identifier
- `limit`: Number of conversations to retrieve (default: 50)

**Response:**
```json
{
  "conversations": [
    {
      "user_message": "Hello",
      "bot_response": "Hi there! How can I help?",
      "timestamp": "2024-01-15T10:30:00"
    }
  ]
}
```

## Customization

### Adding New Intents
Edit `chatbot.py` to add new intent keywords and responses:

```python
self.intent_keywords['new_intent'] = ['keyword1', 'keyword2']
self.faq_responses['new_intent'] = [
    "Response 1",
    "Response 2"
]
```

### Modifying the UI
Edit `templates/index.html` to customize the chat interface appearance and behavior.

### Database Schema
The SQLite database automatically creates a `conversations` table with:
- `id`: Primary key
- `user_id`: User identifier
- `user_message`: User's message
- `bot_response`: Bot's response
- `timestamp`: Message timestamp

## Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production WSGI server (Gunicorn, uWSGI)
2. Configure environment variables
3. Set up a reverse proxy (Nginx)
4. Use a process manager (PM2, Supervisor)

### Environment Variables
- `FLASK_ENV`: Set to 'production' for production
- `DATABASE_URL`: Database connection string (optional)

## Troubleshooting

### Common Issues

1. **Model Download Issues**
   - The first run will download AI models (~500MB)
   - Ensure stable internet connection
   - Check available disk space

2. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill the process using the port

3. **Database Errors**
   - Delete `chatbot.db` to reset the database
   - Check file permissions

### Performance Tips

- Use a GPU for faster sentiment analysis
- Implement caching for frequent queries
- Consider using a production database (PostgreSQL, MySQL)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

---

**Built with ❤️ using Python, Flask, and AI/ML technologies** 