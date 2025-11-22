import gradio as gr
import random
from datetime import datetime
import pandas as pd
import plotly.express as px
import requests
import os
import json

# Hugging Face API configuration
class HuggingFaceAPI:
    def __init__(self):
        # Get API key from environment variable or Gradio secrets
        self.api_key = os.getenv("HF_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.sentiment_api_url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.chat_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    
    def query_sentiment(self, text):
        """Query Hugging Face sentiment analysis model"""
        try:
            payload = {"inputs": text}
            response = requests.post(
                self.sentiment_api_url, 
                headers=self.headers, 
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0]
            return None
        except Exception as e:
            print(f"Sentiment API error: {e}")
            return None
    
    def query_chat(self, text, context=""):
        """Query Hugging Face chat model"""
        try:
            # For DialoGPT or similar models
            prompt = f"{context}\nUser: {text}\nAssistant:"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 100,
                    "temperature": 0.7,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                self.chat_api_url,
                headers=self.headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0]['generated_text']
            return None
        except Exception as e:
            print(f"Chat API error: {e}")
            return None

class MentalWellnessChatbot:
    def __init__(self, use_hf_api=True):
        self.use_hf_api = use_hf_api
        if use_hf_api:
            self.hf_api = HuggingFaceAPI()
        
        self.mood_activities = {
            "sad": [
                "Listen to your favorite music 🎵",
                "Write down three things you're grateful for ✍️",
                "Reach out to a friend or loved one 💕",
                "Watch a comforting movie or show 🎬",
                "Do some gentle stretching or yoga 🧘"
            ],
            "stressed": [
                "Try a 5-minute breathing exercise 🌬️",
                "Take a short walk in nature 🚶‍♂️",
                "Practice 3 minutes of mindfulness meditation 🪷",
                "Make a cup of herbal tea ☕",
                "Do a quick desk stretch routine 💪"
            ],
            "happy": [
                "Share your joy with someone else 😊",
                "Start a gratitude journal 📔",
                "Do something creative like drawing or writing 🎨",
                "Dance to your favorite song 💃",
                "Plan something fun for later 🎉"
            ],
            "angry": [
                "Try some physical exercise 🏃‍♀️",
                "Practice deep breathing for 2 minutes 🌊",
                "Write down your feelings, then tear it up 📝",
                "Squeeze a stress ball or pillow 👐",
                "Count slowly to 10 before responding 🔢"
            ],
            "anxious": [
                "Ground yourself with the 5-4-3-2-1 technique 🌟",
                "Listen to calming music or sounds 🎶",
                "Sip some warm tea slowly 🫖",
                "Do a body scan meditation 👁️",
                "Focus on your breath for one minute 🫁"
            ],
            "tired": [
                "Take a 20-minute power nap 😴",
                "Drink a glass of cold water 💧",
                "Do some light stretching 🏃",
                "Get some fresh air 🌳",
                "Listen to upbeat music 🎧"
            ],
            "neutral": [
                "Practice mindfulness for a few minutes 🪷",
                "Take a moment to appreciate your surroundings 🌸",
                "Do something kind for someone else 💝",
                "Read a few pages of a good book 📚",
                "Plan your next small adventure 🗺️"
            ]
        }
        
        self.mood_history = []
        self.chat_context = ""
    
    def detect_mood_with_hf(self, text):
        """Enhanced mood detection using Hugging Face API"""
        try:
            result = self.hf_api.query_sentiment(text)
            
            if result:
                label = result['label']
                score = result['score']
                
                # Map sentiment labels to moods
                sentiment_to_mood = {
                    'positive': 'happy',
                    'negative': 'sad',
                    'neutral': 'neutral'
                }
                
                base_mood = sentiment_to_mood.get(label, 'neutral')
                
                # Enhanced mood detection based on keywords
                text_lower = text.lower()
                mood_indicators = {
                    'stressed': ['stressed', 'overwhelmed', 'pressure', 'busy'],
                    'anxious': ['anxious', 'nervous', 'worried', 'scared'],
                    'angry': ['angry', 'mad', 'frustrated', 'annoyed'],
                    'tired': ['tired', 'exhausted', 'fatigued', 'sleepy']
                }
                
                for mood, keywords in mood_indicators.items():
                    if any(keyword in text_lower for keyword in keywords):
                        return mood
                
                return base_mood
                
            return self.detect_mood_fallback(text)
            
        except Exception as e:
            print(f"Mood detection error: {e}")
            return self.detect_mood_fallback(text)
    
    def detect_mood_fallback(self, text):
        """Fallback mood detection using keywords"""
        text_lower = text.lower()
        
        mood_keywords = {
            "sad": ["sad", "depressed", "down", "unhappy", "miserable", "blue", "lonely"],
            "stressed": ["stressed", "overwhelmed", "pressure", "busy", "tense", "burnout"],
            "happy": ["happy", "good", "great", "awesome", "wonderful", "joy", "excited"],
            "angry": ["angry", "mad", "frustrated", "annoyed", "irritated", "furious"],
            "anxious": ["anxious", "nervous", "worried", "scared", "panic", "afraid"],
            "tired": ["tired", "exhausted", "fatigued", "sleepy", "drained", "burned out"]
        }
        
        for mood, keywords in mood_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return mood
        
        return "neutral"
    
    def detect_mood(self, text):
        """Main mood detection function"""
        if self.use_hf_api and self.hf_api.api_key:
            return self.detect_mood_with_hf(text)
        else:
            return self.detect_mood_fallback(text)
    
    def generate_ai_response(self, user_message, detected_mood):
        """Generate AI response using Hugging Face API"""
        if not self.use_hf_api or not self.hf_api.api_key:
            return self.get_empathic_response(detected_mood)
        
        try:
            # Create context for the AI
            mood_context = {
                "sad": "The user is feeling sad. Respond with warmth, validation, and gentle encouragement.",
                "stressed": "The user is feeling stressed. Respond with calming, practical suggestions and reassurance.",
                "happy": "The user is feeling happy. Respond with enthusiasm and encouragement to maintain positivity.",
                "angry": "The user is feeling angry. Respond with validation and calming techniques.",
                "anxious": "The user is feeling anxious. Respond with reassurance and grounding techniques.",
                "tired": "The user is feeling tired. Respond with understanding and gentle suggestions for rest.",
                "neutral": "The user seems neutral. Respond with warmth and engaging conversation."
            }
            
            system_prompt = f"You are EmoMood, a compassionate mental wellness assistant. {mood_context.get(detected_mood, 'Be warm and supportive.')} Keep responses under 100 words."
            
            ai_response = self.hf_api.query_chat(user_message, system_prompt)
            
            if ai_response:
                # Clean up the response
                cleaned_response = ai_response.split('\n')[0].strip()
                if cleaned_response and len(cleaned_response) > 10:
                    return cleaned_response
            
            # Fallback to predefined responses
            return self.get_empathic_response(detected_mood)
            
        except Exception as e:
            print(f"AI response error: {e}")
            return self.get_empathic_response(detected_mood)
    
    def get_empathic_response(self, mood):
        """Fallback empathic responses"""
        responses = {
            "sad": "I'm really sorry you're feeling this way. Remember that your feelings are valid, and it's okay to not be okay sometimes. You're not alone in this.",
            "stressed": "I hear that you're carrying a lot right now. Let's take a deep breath together. You're doing better than you think.",
            "happy": "That's absolutely wonderful! Your positivity is contagious. Savor this moment and let it fuel you.",
            "angry": "I understand this frustration. Your feelings are completely valid. Let's find a healthy way to process this energy.",
            "anxious": "I sense the worry weighing on you. Let's ground ourselves in this moment together. You're safe right now.",
            "tired": "It sounds like you really need some rest. Your body and mind are asking for care. Be gentle with yourself today.",
            "neutral": "Thanks for checking in. Sometimes a neutral day is exactly what we need. How can I support you right now?"
        }
        return responses.get(mood, "Thank you for sharing how you're feeling with me.")
    
    def get_activity_suggestions(self, mood, num_suggestions=3):
        """Get random activity suggestions for the detected mood"""
        activities = self.mood_activities.get(mood, self.mood_activities["neutral"])
        return random.sample(activities, min(num_suggestions, len(activities)))
    
    def chat(self, message, chat_history):
        """Main chat function"""
        if not message.strip():
            return chat_history, chat_history, ""
        
        # Detect mood from user message
        detected_mood = self.detect_mood(message)
        
        # Log mood for tracking
        self.mood_history.append({
            "timestamp": datetime.now(),
            "mood": detected_mood,
            "message": message[:50] + "..." if len(message) > 50 else message
        })
        
        # Generate AI response
        ai_response = self.generate_ai_response(message, detected_mood)
        activities = self.get_activity_suggestions(detected_mood)
        
        # Format bot response
        bot_response = f"{ai_response}\n\n"
        bot_response += f"**Detected mood**: {detected_mood.upper()}\n\n"
        bot_response += "**Suggested activities:**\n"
        
        for i, activity in enumerate(activities, 1):
            bot_response += f"• {activity}\n"
        
        # Update chat history
        chat_history.append((message, bot_response))
        
        return chat_history, chat_history, ""  # Return empty string to clear input

    def get_mood_stats(self):
        """Generate basic mood statistics"""
        if not self.mood_history:
            return self.create_empty_plot()
        
        df = pd.DataFrame(self.mood_history)
        mood_counts = df['mood'].value_counts()
        
        # Create visualization
        fig = px.pie(
            values=mood_counts.values, 
            names=mood_counts.index,
            title="Your Mood Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(showlegend=False)
        
        return fig
    
    def create_empty_plot(self):
        """Create empty plot placeholder"""
        fig = px.pie(values=[1], names=["No data yet"], title="Your Mood Distribution")
        fig.update_traces(textposition='inside', textinfo='label')
        fig.update_layout(showlegend=False)
        return fig

# Initialize chatbot
chatbot = MentalWellnessChatbot(use_hf_api=True)

# Quick mood logging function
def quick_mood_log(mood):
    """Quick mood logging with emojis"""
    mood_map = {
        "😊 Happy": "happy",
        "😢 Sad": "sad", 
        "😰 Stressed": "stressed",
        "😠 Angry": "angry",
        "😟 Anxious": "anxious",
        "😴 Tired": "tired",
        "😐 Neutral": "neutral"
    }
    
    detected_mood = mood_map.get(mood, "neutral")
    chatbot.mood_history.append({
        "timestamp": datetime.now(),
        "mood": detected_mood,
        "message": f"Quick log: {mood}"
    })
    
    return f"✅ Logged mood: {mood}"

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="EmoMood - AI Mental Wellness Assistant") as demo:
    gr.Markdown("""
    # 🌈 EmoMood - Your AI Mental Wellness Companion
    
    *Powered by Hugging Face AI models for personalized support*
    """)
    
    with gr.Tab("💬 AI Chat"):
        with gr.Row():
            with gr.Column(scale=2):
                chatbot_interface = gr.Chatbot(
                    value=[("Hello! I'm EmoMood, your AI wellness companion. How are you feeling today?", "")],
                    height=500,
                    show_copy_button=True,
                    bubble_full_width=False
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="Share how you're feeling...",
                        lines=2,
                        container=False,
                        scale=4,
                        max_lines=4
                    )
                    send_btn = gr.Button("Send 💫", variant="primary", scale=1)
            
            with gr.Column(scale=1):
                gr.Markdown("### 🎯 Quick Mood Log")
                quick_mood_selector = gr.Radio(
                    choices=["😊 Happy", "😢 Sad", "😰 Stressed", "😠 Angry", "😟 Anxious", "😴 Tired", "😐 Neutral"],
                    label="How are you feeling right now?",
                    value="😐 Neutral"
                )
                quick_log_btn = gr.Button("Log My Mood 📝")
                quick_log_output = gr.Textbox(label="Status", interactive=False)
                
                gr.Markdown("---")
                gr.Markdown("""
                ### ℹ️ About AI Features
                
                **Powered by Hugging Face models:**
                - 🤖 Advanced mood detection
                - 💬 Empathetic AI conversations  
                - 🎯 Personalized suggestions
                
                *Your data stays private and secure*
                """)
        
        # Connect chat components
        send_btn.click(
            fn=chatbot.chat,
            inputs=[msg, chatbot_interface],
            outputs=[chatbot_interface, chatbot_interface, msg]
        )
        
        msg.submit(
            fn=chatbot.chat,
            inputs=[msg, chatbot_interface],
            outputs=[chatbot_interface, chatbot_interface, msg]
        )
        
        # Connect quick log
        quick_log_btn.click(
            fn=quick_mood_log,
            inputs=[quick_mood_selector],
            outputs=[quick_log_output]
        )
    
    with gr.Tab("📊 Mood Analytics"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Your Mood Trends")
                mood_plot = gr.Plot(label="Mood Distribution")
                update_btn = gr.Button("🔄 Update Analytics")
                
                update_btn.click(
                    fn=chatbot.get_mood_stats,
                    outputs=[mood_plot]
                )
            
            with gr.Column():
                gr.Markdown("### 📈 Recent Mood Log")
                mood_table = gr.Dataframe(
                    headers=["Time", "Mood", "Message"],
                    datatype=["str", "str", "str"],
                    row_count=5,
                    col_count=(3, "fixed")
                )
                
                def get_recent_moods():
                    if not chatbot.mood_history:
                        return pd.DataFrame(columns=["Time", "Mood", "Message"])
                    
                    df = pd.DataFrame(chatbot.mood_history)
                    df['Time'] = df['timestamp'].dt.strftime('%H:%M')
                    return df[['Time', 'Mood', 'Message']].tail(10)
                
                update_btn.click(
                    fn=get_recent_moods,
                    outputs=[mood_table]
                )
    
    with gr.Tab("⚙️ Settings"):
        gr.Markdown("### API Configuration")
        api_status = gr.Textbox(
            label="Hugging Face API Status",
            value="✅ API Integrated" if chatbot.hf_api.api_key else "❌ API Key Not Found",
            interactive=False
        )
        
        gr.Markdown("""
        ### How to set up your API key:
        
        1. Get your Hugging Face token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
        2. In Hugging Face Spaces, go to Settings → Repository secrets
        3. Add secret: `HF_API_KEY = your_token_here`
        
        **Current Features:**
        - Advanced sentiment analysis
        - AI-powered conversations  
        - Personalized mood tracking
        - Activity recommendations
        """)

# For Hugging Face Spaces deployment
if __name__ == "__main__":
    demo.launch(
        share=True,
        show_error=True
    )
