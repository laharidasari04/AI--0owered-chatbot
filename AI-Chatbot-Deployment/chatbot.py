import nltk
import re
import json
import random

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class Chatbot:
    def __init__(self):
        # Simple sentiment analysis using keyword matching
        self.positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 
            'love', 'like', 'enjoy', 'happy', 'joy', 'pleased', 'satisfied', 'perfect',
            'beautiful', 'nice', 'cool', 'sweet', 'brilliant', 'outstanding', 'superb',
            'excited', 'thrilled', 'delighted', 'ecstatic', 'wonderful', 'marvelous'
        ]
        
        self.negative_words = [
            'bad', 'terrible', 'awful', 'horrible', 'disappointing', 'sad', 'angry',
            'hate', 'dislike', 'upset', 'frustrated', 'annoyed', 'worried', 'scared',
            'terrible', 'awful', 'dreadful', 'miserable', 'depressed', 'anxious',
            'stressed', 'tired', 'exhausted', 'overwhelmed', 'confused', 'lost'
        ]
        
        # Enhanced responses with more realistic and diverse options
        self.faq_responses = {
            'greeting': [
                "Hey there! 👋 How's your day going so far?",
                "Hi! Nice to meet you! What brings you here today?",
                "Hello! I'm excited to chat with you. What's on your mind?",
                "Hey! Thanks for stopping by. How can I make your day better?",
                "Hi there! I'm here to help and chat. What would you like to talk about?"
            ],
            'goodbye': [
                "Take care! It was great chatting with you. Come back anytime! 👋",
                "See you later! Hope I was able to help. Have a wonderful day!",
                "Goodbye! Don't hesitate to reach out if you need anything else.",
                "Farewell! It's been a pleasure talking with you. Stay awesome!",
                "Bye for now! Looking forward to our next conversation. Take care!"
            ],
            'thanks': [
                "You're absolutely welcome! 😊 Is there anything else I can help you with?",
                "My pleasure! I'm here to help. What else would you like to explore?",
                "Anytime! I really enjoy our conversations. What's next on your mind?",
                "You're welcome! Helping you makes my day. What else can I assist with?",
                "Glad I could help! I'm always here when you need me. What's up next?"
            ],
            'help': [
                "I'm your AI companion! Here's what I can do:\n\n🎯 **Chat & Connect**: Have meaningful conversations about anything\n🎭 **Entertainment**: Tell jokes, share fun facts, discuss movies/music\n💡 **Learning**: Help with topics like tech, business, education, sports\n😊 **Support**: Listen, provide encouragement, and offer advice\n📚 **Information**: Answer questions and share knowledge\n\nWhat interests you most? I'd love to dive deeper into any of these areas!",
                
                "I'm here to be your friendly AI assistant! My superpowers include:\n\n🤖 **Smart Conversations**: I understand context and remember our chats\n🎪 **Fun & Games**: Jokes, trivia, and entertaining discussions\n📖 **Knowledge Sharing**: Tech, sports, food, travel, and much more\n💬 **Active Listening**: I pick up on your mood and respond accordingly\n🔄 **Memory**: I keep track of our conversation history\n\nWhat would you like to explore together?",
                
                "Think of me as your digital friend! I can:\n\n💭 **Chat Naturally**: Just like talking to a real person\n🎯 **Understand You**: I get what you're saying and respond appropriately\n🌟 **Keep You Engaged**: From serious discussions to lighthearted fun\n📱 **Be Available**: I'm here whenever you need someone to talk to\n🎨 **Adapt**: Whether you want advice, entertainment, or just company\n\nWhat kind of conversation are you in the mood for today?"
            ],
            'weather': [
                "I wish I could check the weather for you! 🌤️ Unfortunately, I don't have access to real-time weather data. But I'd recommend checking your favorite weather app or website for the most accurate forecast. What's the weather like where you are? I'd love to hear about it!",
                "I can't see outside my digital window! 😄 For current weather, try apps like Weather.com, AccuWeather, or your phone's built-in weather app. Are you planning something fun that depends on the weather? I'd love to hear about your plans!"
            ],
            'time': [
                "I don't have a watch, but you can check the time on your device! ⏰ What time is it where you are? I'm curious about your timezone and what you're up to at this hour.",
                "Time flies when you're having fun chatting! 🕐 Check your device for the current time. Are you an early bird or night owl? I'm always here, no matter what time it is!"
            ],
            'joke': [
                "Why don't scientists trust atoms? Because they make up everything! 😄\n\nWant another one? I've got plenty more where that came from!",
                "What do you call a fake noodle? An impasta! 🍝\n\nThat one always cracks me up! Should I tell you another?",
                "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾\n\nCorny, I know, but I love it! Want to hear another?",
                "What do you call a bear with no teeth? A gummy bear! 🐻\n\nThat's one of my favorites! I've got more if you're in the mood for laughs.",
                "Why don't eggs tell jokes? They'd crack each other up! 🥚\n\nEgg-cellent humor, right? 😂 Should I scramble up another one?",
                "What do you call a fish wearing a bowtie? So-fish-ticated! 🐟\n\nI know, I know... fish jokes are a bit fishy! Want another?"
            ],
            'music': [
                "Music is the soundtrack of life! 🎵 I can't play tunes directly, but I love discussing music. What's your favorite genre? Are you into rock, pop, jazz, classical, or something else? I'd love to hear about your musical taste!",
                "I'm always humming digital tunes! 🎶 While I can't stream music, I can chat about artists, genres, and help you discover new sounds. What kind of music gets you moving? Any favorite artists or songs you'd like to discuss?",
                "Music connects us all! 🎼 I can't play songs, but I'm passionate about discussing everything musical. From classical masterpieces to modern hits, what's your jam? I'd love to hear about your musical journey!"
            ],
            'food': [
                "Food is one of life's greatest pleasures! 🍕 I can't cook for you (I'm not very good with kitchen appliances 😄), but I love talking about cuisine! What's your favorite type of food? Are you a foodie who loves trying new dishes?",
                "I may be digital, but I appreciate good food! 🍜 I can help you discuss recipes, restaurants, and culinary adventures. What's your comfort food? Any cuisines you're curious about or want to explore?",
                "Cooking and eating bring so much joy! 🍳 While I can't whip up a meal, I can chat about food all day. Are you a home chef, restaurant explorer, or just someone who appreciates a good meal? What's your food story?"
            ],
            'sports': [
                "Sports bring out the passion in all of us! ⚽ I can't watch games with you, but I love discussing teams, players, and the excitement of competition. What's your favorite sport? Are you a die-hard fan of any particular team?",
                "The thrill of the game is universal! 🏀 I'm a big sports fan too. Whether it's football, basketball, soccer, or any other sport, I'd love to hear about your favorites. Who do you root for? Any memorable games you've watched?",
                "Sports unite people like nothing else! 🏈 I can chat about any sport under the sun. Are you an athlete, a spectator, or just someone who enjoys the energy of sports? What gets you excited about the games?"
            ],
            'technology': [
                "Technology is absolutely fascinating! 🤖 I'm built with some pretty cool tech myself. What aspect interests you most? Are you into programming, AI, gadgets, or just curious about how things work? I'd love to dive deep into any tech topic!",
                "The tech world never stops evolving! 💻 I'm passionate about everything from coding to artificial intelligence. Are you a developer, tech enthusiast, or just someone who's curious about the digital world? What tech topics get you excited?",
                "Technology shapes our future! 🚀 I'm always excited to discuss the latest innovations. Whether it's programming languages, AI developments, or the newest gadgets, what tech area would you like to explore? Are you building anything cool?"
            ],
            'education': [
                "Learning is a lifelong adventure! 📚 I'm always excited to help people discover new knowledge. What subject are you passionate about? Are you a student, teacher, or just someone who loves to learn? I'd love to help you explore any topic!",
                "Education opens so many doors! 🎓 Whether it's formal schooling, online courses, or self-study, I'm here to support your learning journey. What are you studying or interested in learning? Any particular challenges you're facing?",
                "Knowledge is power, and I love sharing it! 📖 I can help with various subjects and learning approaches. Are you currently in school, taking online courses, or just curious about specific topics? What would you like to dive into today?"
            ],
            'business': [
                "The business world is incredibly dynamic! 💼 I'm fascinated by entrepreneurship, career development, and business strategies. Are you an entrepreneur, working professional, or just interested in business topics? What aspect would you like to discuss?",
                "Business and career growth are so important! 🏢 Whether it's startups, corporate life, or personal development, I'd love to help you explore these areas. What's your professional focus? Any business challenges you're working through?",
                "The professional world offers endless possibilities! 💡 I can discuss everything from leadership to innovation. Are you building a business, advancing your career, or just curious about the business world? What would you like to explore?"
            ]
        }
        
        # Keywords for intent recognition
        self.intent_keywords = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening'],
            'goodbye': ['bye', 'goodbye', 'see you', 'farewell', 'take care'],
            'thanks': ['thank', 'thanks', 'appreciate', 'grateful'],
            'help': ['help', 'assist', 'support', 'what can you do', 'functionality', 'functionalities', 'capabilities'],
            'weather': ['weather', 'temperature', 'forecast', 'rain', 'sunny'],
            'time': ['time', 'clock', 'hour', 'minute'],
            'joke': ['joke', 'funny', 'humor', 'laugh', 'tell me a joke'],
            'music': ['music', 'song', 'play', 'artist', 'album'],
            'food': ['food', 'eat', 'restaurant', 'meal', 'hungry'],
            'sports': ['sports', 'game', 'team', 'player', 'match'],
            'technology': ['technology', 'computer', 'software', 'programming', 'code'],
            'education': ['learn', 'study', 'education', 'school', 'university'],
            'business': ['business', 'work', 'job', 'career', 'company']
        }
    
    def preprocess_text(self, text):
        """Clean and normalize the input text"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def detect_intent(self, text):
        """Detect the intent of the user message"""
        text = self.preprocess_text(text)
        words = text.split()
        
        # Check for exact matches first
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    return intent
        
        # Check for partial matches and common variations
        text_lower = text.lower()
        
        # Help/functionality detection
        if any(word in text_lower for word in ['functionality', 'functionalities', 'functionlities', 'capabilities', 'what can you do', 'what do you do', 'what are your']):
            return 'help'
        
        # Joke detection
        if any(word in text_lower for word in ['joke', 'funny', 'humor', 'laugh', 'tell me a joke', 'make me laugh']):
            return 'joke'
        
        # Technology detection
        if any(word in text_lower for word in ['technology', 'computer', 'software', 'programming', 'code', 'ai', 'artificial intelligence']):
            return 'technology'
        
        # Education detection
        if any(word in text_lower for word in ['learn', 'study', 'education', 'school', 'university', 'course', 'training']):
            return 'education'
        
        # Business detection
        if any(word in text_lower for word in ['business', 'work', 'job', 'career', 'company', 'professional']):
            return 'business'
        
        return 'general'
    
    def get_sentiment(self, text):
        """Analyze the sentiment of the user message using simple keyword matching"""
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        
        if positive_count > negative_count:
            return 'POSITIVE'
        elif negative_count > positive_count:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'
    
    def generate_contextual_response(self, text, intent, sentiment):
        """Generate a contextual response based on intent and sentiment"""
        if intent in self.faq_responses:
            response = random.choice(self.faq_responses[intent])
        else:
            # Generate more intelligent and realistic responses for general queries
            text_lower = text.lower()
            
            # Check for question words
            if any(word in text_lower for word in ['what', 'how', 'why', 'when', 'where', 'who']):
                if 'what' in text_lower:
                    response = "That's a really interesting question! 🤔 I'd love to help you explore that topic. Could you give me a bit more context so I can provide you with the most helpful answer possible? What specifically are you curious about?"
                elif 'how' in text_lower:
                    response = "Great question! I'd be happy to help you figure that out. Could you tell me a bit more about what you're trying to accomplish? The more details you share, the better I can assist you! 😊"
                elif 'why' in text_lower:
                    response = "That's such a thoughtful question! I'd love to dive into that with you. What aspect of this topic interests you most? Understanding your perspective will help me give you a more meaningful response."
                else:
                    response = "I'm really curious about that too! 🤓 Could you share a bit more about what you'd like to know? I want to make sure I give you the most helpful and relevant information possible."
            
            # Check for specific topics with more engaging responses
            elif any(word in text_lower for word in ['movie', 'film', 'cinema']):
                response = "Movies are absolutely magical! 🎬 I love discussing everything from blockbusters to indie films. What genres do you enjoy? Are you more into action-packed adventures, heartwarming dramas, or maybe something that makes you think? I'd love to hear about your favorite films!"
            
            elif any(word in text_lower for word in ['book', 'read', 'novel', 'author']):
                response = "Books are like windows to other worlds! 📚 I'm always excited to talk about literature. What kind of stories capture your imagination? Are you into fiction, non-fiction, or maybe a bit of both? I'd love to hear about what you're reading or what you'd like to explore!"
            
            elif any(word in text_lower for word in ['travel', 'trip', 'vacation', 'destination']):
                response = "Travel is one of life's greatest adventures! ✈️ I love hearing about people's journeys and dreams. Where have you been that you absolutely loved? Or is there a place you're dreaming of visiting? I'd love to hear about your travel experiences or help you plan your next adventure!"
            
            elif any(word in text_lower for word in ['health', 'fitness', 'exercise', 'workout']):
                response = "Taking care of yourself is so important! 💪 I'm passionate about health and wellness. What's your approach to staying healthy? Are you into specific types of exercise, nutrition, or just maintaining a balanced lifestyle? I'd love to hear about your wellness journey!"
            
            elif any(word in text_lower for word in ['art', 'painting', 'drawing', 'creative']):
                response = "Art is such a beautiful way to express yourself! 🎨 I'm fascinated by all forms of creativity. Are you an artist yourself, or do you just appreciate beautiful things? What kind of art speaks to you? I'd love to hear about your creative interests!"
            
            # Enhanced sentiment-based responses
            elif sentiment == 'POSITIVE':
                responses = [
                    "That's absolutely wonderful! 😊 I can feel your positive energy through the screen. What's making you feel so great? I'd love to hear more about what's bringing you joy right now!",
                    "That's fantastic! 🌟 Your enthusiasm is contagious. I'm so glad you're feeling good. What else is going well in your life? I'd love to celebrate the good things with you!",
                    "That's amazing! ✨ I'm genuinely happy to hear that. Positive vibes are the best! What would you like to explore or accomplish while you're in such a great mood?",
                    "That's so uplifting! 🎉 I love when people are feeling their best. What's the highlight of your day so far? I'd love to hear about what's making you smile!"
                ]
                response = random.choice(responses)
            
            elif sentiment == 'NEGATIVE':
                responses = [
                    "I hear you, and I want you to know that it's okay to feel this way. 💙 Sometimes things can be really tough, and I'm here to listen. Would you like to talk about what's going on? Sometimes just sharing can help lighten the load.",
                    "I can sense that you're going through something difficult, and I want you to know that you're not alone. 🤗 It's completely normal to have rough patches. What's on your mind? I'm here to listen and support you however I can.",
                    "I understand that things might feel overwhelming right now, and I want you to know that your feelings are valid. 💜 Sometimes we all need someone to talk to. What would be most helpful for you right now - someone to listen, or maybe some gentle encouragement?",
                    "I'm sorry you're feeling this way, and I want you to know that I care. 💚 Everyone goes through difficult times, and it's okay to not be okay. What's happening? I'm here to listen and help you work through this."
                ]
                response = random.choice(responses)
            
            else:
                # Enhanced neutral sentiment responses
                responses = [
                    "That's really interesting! 🤔 I'd love to explore that topic with you. What specific aspect would you like to dive into? I'm curious to hear your thoughts and share what I know!",
                    "That's a great point! I'm genuinely interested in learning more about your perspective. What questions do you have about this? I'd love to help you discover more about this topic.",
                    "That's fascinating! I'd be happy to help you explore that further. What would you like to know more about? I want to make sure I give you the most helpful and relevant information possible.",
                    "That's an excellent topic to discuss! I'm excited to help you learn more about that. What specific aspect interests you most? I'd love to share what I know and hear your thoughts too!",
                    "That's really worth exploring! I'd be happy to help you understand that better. What would you like to focus on? I want to make sure our conversation is as helpful and engaging as possible for you."
                ]
                response = random.choice(responses)
        
        return response
    
    def get_response(self, user_message):
        """Main method to get chatbot response"""
        if not user_message.strip():
            return "I didn't quite catch that. Could you please repeat what you said? I want to make sure I understand you properly! 😊"
        
        # Detect intent
        intent = self.detect_intent(user_message)
        
        # Analyze sentiment
        sentiment = self.get_sentiment(user_message)
        
        # Generate response
        response = self.generate_contextual_response(user_message, intent, sentiment)
        
        return response
    
    def get_conversation_summary(self, conversations):
        """Generate a summary of conversation history"""
        if not conversations:
            return "No previous conversations found yet. I'm looking forward to our first chat! 😊"
        
        total_messages = len(conversations)
        user_messages = [conv['user_message'] for conv in conversations]
        
        # Analyze overall sentiment
        sentiments = []
        for message in user_messages:
            sentiment = self.get_sentiment(message)
            sentiments.append(sentiment)
        
        positive_count = sentiments.count('POSITIVE')
        negative_count = sentiments.count('NEGATIVE')
        neutral_count = sentiments.count('NEUTRAL')
        
        summary = f"📊 **Our Conversation Summary:**\n\n"
        summary += f"💬 **Total messages exchanged**: {total_messages}\n"
        summary += f"😊 **Positive moments**: {positive_count}\n"
        summary += f"😔 **Challenging moments**: {negative_count}\n"
        summary += f"😐 **Neutral exchanges**: {neutral_count}\n\n"
        
        if positive_count > negative_count:
            summary += "🌟 **Overall vibe**: You seem to be in a really positive mood! I love our uplifting conversations! 😊"
        elif negative_count > positive_count:
            summary += "💙 **Overall vibe**: I've noticed you've been going through some tough times. I'm here to support you through it all. 🤗"
        else:
            summary += "🤔 **Overall vibe**: We've had some great balanced conversations! I enjoy our thoughtful discussions. 😊"
        
        return summary 