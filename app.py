
# pip install -q gradio pandas plotly

import gradio as gr
import datetime
import pandas as pd
import plotly.express as px
import random
from typing import Dict, List
import re

class MentalWellnessWebsite:
    def __init__(self):
        self.mood_history = []
        self.activity_log = []
        
        # Enhanced crisis detection keywords
        self.crisis_keywords = [
            'suicide', 'kill myself', 'end it all', 'want to die', 'harm myself',
            'ending my life', 'no reason to live', 'better off dead', 'marny ka',
            'marne ka', 'zindagi khatam', 'jeene ka man nahi', 'suicidal',
            'end my life', 'no point living', 'want to disappear', 'self harm',
            'cut myself', 'hurt myself', 'give up on life'
        ]
        
        # Comprehensive emotion database
        self.emotion_data = {
            "anxious": {
                "name": "Anxiety",
                "emoji": "😰",
                "description": "Feeling worried, nervous, or uneasy",
                "motivational_messages": [
                    "Breathe deeply. This anxious moment will pass, just like all the others before it.",
                    "Your anxiety is not a permanent state. Each breath you take is moving you toward calm.",
                    "You've survived every anxious moment until now. You will survive this one too.",
                    "Anxiety is just your body's way of saying it cares deeply. Let's channel that care positively."
                ],
                "activities": [
                    {"name": "5-Minute Breathing", "duration": "5 min", "emoji": "🌬️", "description": "Box breathing: inhale 4s, hold 4s, exhale 4s"},
                    {"name": "Grounding Exercise", "duration": "3 min", "emoji": "🌍", "description": "Name 5 things you can see, 4 you can touch, 3 you can hear"},
                    {"name": "Progressive Relaxation", "duration": "7 min", "emoji": "💆", "description": "Tense and relax each muscle group from toes to head"},
                    {"name": "Anxiety Journal", "duration": "10 min", "emoji": "📝", "description": "Write down your worries and challenge each one"},
                    {"name": "Calming Walk", "duration": "15 min", "emoji": "🚶", "description": "Walk slowly while focusing on your surroundings"}
                ],
                "color": "#FFB74D"
            },
            "depressed": {
                "name": "Sadness",
                "emoji": "😔",
                "description": "Feeling down, hopeless, or low energy",
                "motivational_messages": [
                    "Even on your darkest days, you are still worthy of love and care.",
                    "This heavy feeling is temporary. Brighter moments are waiting for you.",
                    "You don't have to be productive to be valuable. Rest is productive too.",
                    "The fact that you're still here shows incredible strength. I'm proud of you."
                ],
                "activities": [
                    {"name": "Gratitude List", "duration": "5 min", "emoji": "🙏", "description": "Write 3 small things you're grateful for today"},
                    {"name": "Comfort Movie", "duration": "90 min", "emoji": "🎬", "description": "Watch a movie that always makes you feel safe"},
                    {"name": "Gentle Stretching", "duration": "10 min", "emoji": "🧘", "description": "Simple stretches while breathing deeply"},
                    {"name": "Connect with Nature", "duration": "15 min", "emoji": "🌳", "description": "Sit outside or look out a window at nature"},
                    {"name": "Self-Compassion Break", "duration": "5 min", "emoji": "💝", "description": "Place hand on heart and speak kindly to yourself"}
                ],
                "color": "#64B5F6"
            },
            "angry": {
                "name": "Anger",
                "emoji": "😠",
                "description": "Feeling frustrated, irritated, or mad",
                "motivational_messages": [
                    "Your anger shows you care deeply. Let's find a constructive way to express that care.",
                    "It's okay to feel angry. What matters is what you do with that energy.",
                    "Anger is often a signal that a boundary has been crossed. Let's honor that signal.",
                    "This fiery feeling will cool. Give yourself space to process it safely."
                ],
                "activities": [
                    {"name": "Punching Pillows", "duration": "5 min", "emoji": "🥊", "description": "Safely release physical tension with pillows"},
                    {"name": "Anger Journal", "duration": "10 min", "emoji": "📝", "description": "Write everything you feel without filtering"},
                    {"name": "Cold Water Splash", "duration": "2 min", "emoji": "💧", "description": "Splash cold water on your face to reset nervous system"},
                    {"name": "Intense Exercise", "duration": "15 min", "emoji": "💪", "description": "Jumping jacks, running in place, or push-ups"},
                    {"name": "Mindful Counting", "duration": "3 min", "emoji": "🔢", "description": "Count slowly to 100 while breathing deeply"}
                ],
                "color": "#E57373"
            },
            "stressed": {
                "name": "Stress",
                "emoji": "😫",
                "description": "Feeling overwhelmed, pressured, or burnt out",
                "motivational_messages": [
                    "You're carrying a lot right now. It's okay to set some things down.",
                    "Stress is temporary. You've handled difficult times before.",
                    "One thing at a time. You don't have to solve everything right now.",
                    "Your worth isn't measured by your productivity. You matter just as you are."
                ],
                "activities": [
                    {"name": "Priority Sorting", "duration": "10 min", "emoji": "📋", "description": "List everything and circle only top 3 priorities"},
                    {"name": "Mini Meditation", "duration": "5 min", "emoji": "🧘", "description": "Focus only on your breath, let thoughts pass by"},
                    {"name": "Desk Stretch", "duration": "3 min", "emoji": "💺", "description": "Neck rolls, shoulder stretches, wrist circles"},
                    {"name": "Tea Break", "duration": "10 min", "emoji": "🍵", "description": "Make tea mindfully and drink without distractions"},
                    {"name": "Digital Detox", "duration": "30 min", "emoji": "📵", "description": "Turn off all screens and be present"}
                ],
                "color": "#BA68C8"
            },
            "happy": {
                "name": "Happiness",
                "emoji": "😊",
                "description": "Feeling joyful, content, or positive",
                "motivational_messages": [
                    "Savor this beautiful moment! Your joy is contagious and well-deserved.",
                    "Happiness grows when shared. Who can you spread this feeling to?",
                    "This positive energy is fuel for your soul. Enjoy every second of it!",
                    "Your happiness matters. Let it fill you up and overflow to others."
                ],
                "activities": [
                    {"name": "Gratitude Sharing", "duration": "10 min", "emoji": "💌", "description": "Share your happy feelings with someone you care about"},
                    {"name": "Dance Break", "duration": "5 min", "emoji": "💃", "description": "Put on your favorite song and dance like nobody's watching"},
                    {"name": "Creative Expression", "duration": "20 min", "emoji": "🎨", "description": "Draw, write, or create something that captures this joy"},
                    {"name": "Nature Celebration", "duration": "15 min", "emoji": "🌞", "description": "Go outside and fully appreciate the beauty around you"},
                    {"name": "Kindness Ripple", "duration": "10 min", "emoji": "🌟", "description": "Do something kind for someone else to spread the happiness"}
                ],
                "color": "#4CAF50"
            },
            "tired": {
                "name": "Fatigue",
                "emoji": "😴",
                "description": "Feeling exhausted, drained, or low energy",
                "motivational_messages": [
                    "Rest is not lazy - it's essential. Your body is asking for what it needs.",
                    "Even small steps forward are progress when you're tired. Be gentle with yourself.",
                    "Your energy will return. For now, honor your need for rest and recovery.",
                    "You don't have to be productive to be worthy. Your existence is enough."
                ],
                "activities": [
                    {"name": "Power Nap", "duration": "20 min", "emoji": "💤", "description": "Set timer for 20 minutes for optimal energy boost"},
                    {"name": "Hydration Break", "duration": "5 min", "emoji": "💧", "description": "Drink a full glass of water with mindful sips"},
                    {"name": "Gentle Movement", "duration": "5 min", "emoji": "🔄", "description": "Slow stretches or walking around the room"},
                    {"name": "Nourishing Snack", "duration": "10 min", "emoji": "🍎", "description": "Eat something energizing like fruit or nuts"},
                    {"name": "Restful Environment", "duration": "5 min", "emoji": "🌙", "description": "Dim lights, comfortable position, deep breathing"}
                ],
                "color": "#78909C"
            }
        }

    def analyze_emotion(self, text: str) -> Dict:
        """Analyze text to detect emotion with enhanced crisis detection"""
        text_lower = text.lower()
        
        # Enhanced crisis detection
        if any(keyword in text_lower for keyword in self.crisis_keywords):
            return {"emotion": "crisis", "confidence": 0.95}
        
        # Emotion scoring
        emotion_scores = {}
        for emotion, data in self.emotion_data.items():
            score = 0
            
            # Check for emotion keywords
            if emotion in text_lower:
                score += 3
            if data['name'].lower() in text_lower:
                score += 2
            
            # Check for related words
            if emotion == "anxious" and any(w in text_lower for w in ['worry', 'nervous', 'panic', 'scared', 'anxiety']):
                score += 2
            elif emotion == "depressed" and any(w in text_lower for w in ['sad', 'hopeless', 'empty', 'down', 'depression']):
                score += 2
            elif emotion == "angry" and any(w in text_lower for w in ['mad', 'furious', 'frustrated', 'annoyed', 'anger']):
                score += 2
            elif emotion == "stressed" and any(w in text_lower for w in ['overwhelmed', 'pressure', 'burnt out', 'too much', 'stress']):
                score += 2
            elif emotion == "happy" and any(w in text_lower for w in ['good', 'great', 'joy', 'excited', 'wonderful', 'happy']):
                score += 2
            elif emotion == "tired" and any(w in text_lower for w in ['exhausted', 'fatigued', 'drained', 'no energy', 'tired']):
                score += 2
                
            if score > 0:
                emotion_scores[emotion] = score
        
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            return {"emotion": primary_emotion, "confidence": emotion_scores[primary_emotion] / 10.0}
        else:
            return {"emotion": "neutral", "confidence": 0.3}

    def get_motivational_message(self, emotion: str) -> str:
        """Get random motivational message for emotion"""
        if emotion in self.emotion_data:
            return random.choice(self.emotion_data[emotion]['motivational_messages'])
        return "You're doing the best you can, and that's enough. I'm here for you."

    def get_activities(self, emotion: str, count: int = 3) -> List[Dict]:
        """Get recommended activities for emotion"""
        if emotion in self.emotion_data:
            activities = self.emotion_data[emotion]['activities'].copy()
            random.shuffle(activities)
            return activities[:count]
        return []

    def generate_crisis_response(self) -> str:
        """Generate comprehensive crisis response emphasizing life's value and nature's healing"""
        
        life_affirmations = [
            "🌅 **Your life is a unique, irreplaceable story** that's still being written. The world needs your light, even when you can't see it yourself.",
            "💫 **You matter more than you know**. The pain you feel right now is real, but it is not permanent. Brighter days will come.",
            "🌱 **Like a seed in winter**, you may not see growth right now, but incredible transformation is happening beneath the surface.",
            "🌟 **Your existence touches others** in ways you may never fully know. Your absence would leave a space that no one else could fill.",
            "🌊 **Feelings are like waves** - they rise, they crash, and they recede. This overwhelming moment will pass."
        ]
        
        nature_healing = [
            "🌳 **Nature's Healing Power**: Step outside and feel the sun on your skin. Notice how the world continues its beautiful cycles, reminding us that renewal is always possible.",
            "🌿 **Ground Yourself**: Sit with your back against a tree. Feel its strength and stability. Remember that you too have deep roots of resilience.",
            "🐦 **Listen to Life**: Hear the birds singing their songs without worry. They remind us that each being has a unique purpose and voice.",
            "🌄 **Watch a Sunrise/Sunset**: Witness how even the darkest night always gives way to light. Your current darkness will too.",
            "💧 **Water's Wisdom**: Watch water flow around obstacles rather than fighting them. Sometimes surrender to the moment is the bravest choice."
        ]
        
        hopeful_activities = [
            "**🌻 Plant Something**: Even a small seed in a pot. Watch life begin anew and remember your own capacity for growth.",
            "**📝 Write a Letter**: To your future self, describing the beautiful moments you still want to experience.",
            "**🎨 Create Something**: A drawing, poem, or song expressing the pain AND the hope you carry.",
            "**🤗 Reach Out**: Text someone 'I'm having a hard time' or call a helpline. You don't have to carry this alone.",
            "**🌿 Nature Walk**: Walk slowly, noticing 5 beautiful things in nature you haven't seen before."
        ]
        
        affirmation = random.choice(life_affirmations)
        nature_message = random.choice(nature_healing)
        activity = random.choice(hopeful_activities)
        
        crisis_response = f"""
🚨 **I'm deeply concerned about what you're sharing**

{affirmation}

## 🌍 **The Healing Power of Nature**
{nature_message}

## 💝 **Your Life Has Purpose**
- **You are not defined by this pain** - it's a moment in time, not your whole story
- **The world needs your unique perspective** - no one sees things exactly like you do
- **Future you exists** and will thank present you for staying
- **Small moments of beauty await you** - a perfect cup of tea, a child's laughter, a favorite song

## 🆘 **IMMEDIATE HELP - PLEASE REACH OUT NOW:**

### 📞 **24/7 Crisis Support:**
• **988** Suicide & Crisis Lifeline (Call or Text)
• **741741** Crisis Text Line (Text HOME)
• **911** Emergency Services

### 🌟 **Right Now, Try This:**
{activity}

## 🌈 **Remember:**
**This intense pain is temporary.** Millions have stood where you are and found their way to healing. Professional help works, and there are people waiting to support you right now.

**Your story isn't over. Beautiful chapters are still unwritten.** Please reach out for human support immediately.
"""
        return crisis_response

    def log_mood(self, emotion: str, text: str):
        """Log mood entry"""
        entry = {
            "timestamp": datetime.datetime.now(),
            "emotion": emotion,
            "text": text[:100],
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.datetime.now().strftime("%H:%M")
        }
        self.mood_history.append(entry)

    def log_activity(self, activity_name: str, emotion: str):
        """Log completed activity"""
        entry = {
            "timestamp": datetime.datetime.now(),
            "activity": activity_name,
            "emotion": emotion,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.datetime.now().strftime("%H:%M")
        }
        self.activity_log.append(entry)

    def get_mood_stats(self):
        """Get mood statistics for dashboard"""
        if not self.mood_history:
            return None, None
        
        df = pd.DataFrame(self.mood_history)
        
        # Create a numeric value for emotions for the chart
        emotion_map = {emotion: i for i, emotion in enumerate(self.emotion_data.keys())}
        df['emotion_value'] = df['emotion'].map(emotion_map).fillna(len(emotion_map))
        
        # Weekly mood chart
        fig_mood = px.line(df, x='timestamp', y='emotion_value', 
                          title='Your Mood Journey',
                          labels={'timestamp': 'Time', 'emotion_value': 'Mood Level'})
        
        # Emotion distribution
        emotion_counts = df['emotion'].value_counts()
        fig_dist = px.pie(values=emotion_counts.values, names=emotion_counts.index,
                         title='Emotion Distribution')
        
        return fig_mood, fig_dist

# Initialize the wellness system
wellness_system = MentalWellnessWebsite()

def create_app():
    """Create the Gradio application"""
    
    with gr.Blocks(
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="green",
        ),
        title="MindWell - Mental Wellness Companion",
        css="""
        .emotion-emoji { font-size: 4em !important; text-align: center !important; }
        .gradio-container { max-width: 1200px !important; margin: 0 auto !important; }
        .activity-btn { margin: 5px !important; }
        .crisis-response { background-color: #fff3cd; padding: 20px; border-radius: 10px; border-left: 5px solid #ff6b6b; }
        """
    ) as demo:
        
        gr.Markdown("""
        # 🌈 MindWell - Your Mental Wellness Companion
        
        *Your safe space for emotional support, crisis help, and healing through nature*
        """)
        
        with gr.Tabs() as tabs:
            with gr.TabItem("💬 Emotional Support"):
                gr.Markdown("""
                # 💬 How are you feeling today?
                *Share what's on your mind - I'm here to listen and support you*
                """)
                
                with gr.Row():
                    with gr.Column(scale=2):
                        emotion_input = gr.Textbox(
                            label="Share your feelings...",
                            placeholder="I'm feeling anxious about work... I'm really happy because... I'm struggling with...",
                            lines=3,
                            max_lines=5
                        )
                        
                        analyze_btn = gr.Button("Get Support 🌟", size="lg", variant="primary")
                        
                    with gr.Column(scale=1):
                        gr.Markdown("""
                        ### 💡 Examples to try:
                        - "I'm overwhelmed with work deadlines"
                        - "Feeling sad and lonely today"  
                        - "So happy about good news!"
                        - "Stressed about family issues"
                        - "I'm having dark thoughts"
                        """)
                
                # Results section
                with gr.Row(visible=False) as results_row:
                    with gr.Column():
                        emotion_display = gr.Markdown(label="Emotion Analysis")
                        
                        with gr.Row():
                            with gr.Column():
                                motivational_section = gr.Markdown(label="Motivational Message")
                            with gr.Column():
                                emotion_emoji = gr.Markdown(label="Emotion", elem_classes="emotion-emoji")
                        
                        activities_section = gr.Markdown(label="Recommended Activities")
                        
                        with gr.Row() as activities_row:
                            activity_components = []
                            for i in range(3):
                                with gr.Column():
                                    activity_btn = gr.Button(f"Activity {i+1}", visible=False, size="sm", elem_classes="activity-btn")
                                    activity_components.append(activity_btn)
                
                # Crisis section
                with gr.Row(visible=False) as crisis_row:
                    with gr.Column():
                        crisis_display = gr.Markdown(label="Crisis Support", elem_classes="crisis-response")
            
            with gr.TabItem("📊 Wellness Dashboard"):
                gr.Markdown("# 📊 Your Wellness Dashboard")
                
                with gr.Row():
                    with gr.Column():
                        stats_display = gr.Markdown()
                        refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="primary")
                    
                with gr.Row():
                    with gr.Column():
                        mood_chart = gr.Plot(label="Mood Journey")
                    with gr.Column():
                        dist_chart = gr.Plot(label="Emotion Patterns")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("### 📝 Recent Mood Entries")
                        mood_table = gr.Dataframe(
                            headers=["Time", "Emotion", "Note"],
                            datatype=["str", "str", "str"],
                            interactive=False,
                            wrap=True
                        )
                    
                    with gr.Column():
                        gr.Markdown("### ✅ Completed Activities")
                        activity_table = gr.Dataframe(
                            headers=["Time", "Activity", "Mood"],
                            datatype=["str", "str", "str"],
                            interactive=False,
                            wrap=True
                        )
            
            with gr.TabItem("🌿 Nature Healing"):
                gr.Markdown("# 🌿 Healing Through Nature")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown("""
                        ## 🌳 Why Nature Heals
                        
                        **Science shows that spending time in nature:**
                        - Reduces stress and anxiety
                        - Lowers blood pressure
                        - Improves mood and mental clarity
                        - Boosts immune system function
                        - Increases feelings of connection and purpose
                        """)
                        
                        gr.Markdown("""
                        ## 🍃 Simple Nature Practices
                        
                        ### 🌅 Morning Grounding
                        Step outside for 5 minutes each morning. Feel the air, listen to birds, notice the light.
                        
                        ### 🌿 Mindful Walking
                        Walk slowly without destination. Notice textures, colors, smells around you.
                        
                        ### 🌸 Seasonal Awareness
                        Track nature's changes - budding leaves, falling snow, migrating birds.
                        
                        ### 💧 Water Connection
                        Visit water - ocean, river, or even a fountain. Water has calming properties.
                        """)
                    
                    with gr.Column():
                        gr.Markdown("""
                        ## 🌻 Life-Affirming Activities
                        
                        ### Plant & Grow
                        - Start a small herb garden
                        - Grow flowers from seeds
                        - Care for a houseplant
                        
                        ### Nature Journal
                        - Sketch leaves or clouds
                        - Write about seasonal changes
                        - Record bird sightings
                        
                        ### Outdoor Mindfulness
                        - Cloud watching
                        - Star gazing
                        - Listening to rain
                        
                        ### Community Nature
                        - Join a gardening group
                        - Volunteer for park cleanup
                        - Birdwatching with friends
                        """)
                        
                        gr.Markdown("""
                        ## 🌈 Your Life Matters
                        
                        **Remember:**
                        - You are part of nature's beautiful tapestry
                        - Each season teaches us about cycles and renewal
                        - Your unique perspective enriches the world
                        - Future generations need your light
                        """)
        
        # Event handlers for Emotional Support tab
        def process_emotion(text):
            if not text.strip():
                return [
                    gr.update(visible=False),  # results_row
                    gr.update(visible=False),  # crisis_row
                    "", "", "", "", 
                    *[gr.update(visible=False) for _ in range(3)]
                ]
            
            analysis = wellness_system.analyze_emotion(text)
            emotion = analysis['emotion']
            
            if emotion == "crisis":
                crisis_content = wellness_system.generate_crisis_response()
                return [
                    gr.update(visible=False),
                    gr.update(visible=True),
                    "", "", "", crisis_content,
                    *[gr.update(visible=False) for _ in range(3)]
                ]
            
            # Regular emotion processing
            emotion_data = wellness_system.emotion_data.get(emotion, wellness_system.emotion_data["anxious"])
            wellness_system.log_mood(emotion, text)
            
            emotion_display_content = f"""
            ## {emotion_data['emoji']} You're feeling {emotion_data['name']}
            *{emotion_data['description']}*
            """
            
            motivational_message = wellness_system.get_motivational_message(emotion)
            motivational_content = f"""
            ### 💫 Encouragement:
            {motivational_message}
            """
            
            emoji_content = f"# {emotion_data['emoji']}"
            
            activities = wellness_system.get_activities(emotion, 3)
            activities_content = "### 🛠️ Helpful Activities:"
            
            activity_updates = []
            for i, activity in enumerate(activities):
                activity_btn_text = f"{activity['emoji']} {activity['name']} ({activity['duration']})"
                activity_updates.append(gr.update(
                    visible=True, 
                    value=activity_btn_text,
                    interactive=True
                ))
                activities_content += f"\n{i+1}. **{activity['name']}** ({activity['duration']}) - {activity['description']}"
            
            # Fill remaining slots if less than 3 activities
            while len(activity_updates) < 3:
                activity_updates.append(gr.update(visible=False))
            
            return [
                gr.update(visible=True),
                gr.update(visible=False),
                emotion_display_content,
                motivational_content,
                emoji_content,
                activities_content,
                *activity_updates
            ]
        
        def complete_activity(activity_text, emotion):
            """Handle activity completion"""
            activity_name = activity_text.split(')')[0].split(' ')[1] if ')' in activity_text else activity_text
            wellness_system.log_activity(activity_name, emotion)
            return f"✅ Completed: {activity_name}! Great job taking care of yourself. 🌟"
        
        def update_dashboard():
            """Update dashboard with current data"""
            # Mood statistics
            total_moods = len(wellness_system.mood_history)
            total_activities = len(wellness_system.activity_log)
            
            if total_moods > 0:
                recent_moods = wellness_system.mood_history[-5:][::-1]
                mood_data = [[m['time'], m['emotion'].title(), m['text']] for m in recent_moods]
                
                recent_activities = wellness_system.activity_log[-5:][::-1]
                activity_data = [[a['time'], a['activity'], a['emotion'].title()] for a in recent_activities]
                
                fig_mood, fig_dist = wellness_system.get_mood_stats()
                
                stats_text = f"""
                ## 📈 Your Wellness Stats
                - **Total Mood Entries**: {total_moods}
                - **Activities Completed**: {total_activities}
                - **Emotions Tracked**: {len(set(m['emotion'] for m in wellness_system.mood_history))}
                - **Consistency**: {"Great! 🎉" if total_moods >= 3 else "Keep going! 💫"}
                """
            else:
                mood_data = []
                activity_data = []
                fig_mood, fig_dist = None, None
                stats_text = "## 📈 Your Wellness Stats\nStart tracking your moods to see your dashboard come to life! 💫"
            
            return stats_text, fig_mood, fig_dist, mood_data, activity_data
        
        # Connect event handlers
        analyze_btn.click(
            fn=process_emotion,
            inputs=[emotion_input],
            outputs=[
                results_row, crisis_row, emotion_display, 
                motivational_section, emotion_emoji, activities_section,
                *activity_components
            ]
        )
        
        # Activity completion handlers
        for i, activity_btn in enumerate(activity_components):
            activity_btn.click(
                fn=complete_activity,
                inputs=[activity_btn, emotion_display],
                outputs=[activity_btn]
            )
        
        refresh_btn.click(
            fn=update_dashboard,
            outputs=[stats_display, mood_chart, dist_chart, mood_table, activity_table]
        )
        
        # Initial dashboard load
        demo.load(
            fn=update_dashboard,
            outputs=[stats_display, mood_chart, dist_chart, mood_table, activity_table]
        )
    
    return demo

# Function to launch the app in Colab
def launch_in_colab():
    """Launch the app with Colab-friendly settings"""
    print("🚀 Starting Enhanced MindWell Mental Wellness Website...")
    print("⏳ This may take a few seconds...")
    print("✅ Enhanced crisis support with nature healing activated")
    
    # Create the app
    demo = create_app()
    
    # Launch with Colab-friendly settings
    try:
        demo.launch(share=True, debug=False, show_error=True)
    except Exception as e:
        print(f"⚠️  Public link failed, trying local: {e}")
        try:
            demo.launch(server_name="0.0.0.0", server_port=0, debug=False)
        except Exception as e2:
            print(f"🔧 Trying alternative approach...")
            demo.queue()
            demo.launch(share=True, inbrowser=False, quiet=True)

# Run the application
if __name__ == "__main__":
    launch_in_colab()
