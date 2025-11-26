import streamlit as st

# Set page config FIRST before any other Streamlit commands
st.set_page_config(page_title="Forever Fit", layout="wide")

import cv2
from dotenv import load_dotenv
load_dotenv()
import tempfile
import time
import numpy as np
import os
import threading
from datetime import datetime, timedelta
from ui_utils import apply_legendary_styles, render_legendary_header, card_container, render_status_badge

# DeepSeek integration flag
DEEPSEEK_AVAILABLE = False
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if DEEPSEEK_API_KEY:
    DEEPSEEK_AVAILABLE = True
    print("DeepSeek API key detected – advanced reasoning enabled.")

# Import modules with try-except to handle missing dependencies
try:
    import ExerciseAiTrainer as exercise
    from exercise_coach import ExerciseCoach

    EXERCISE_AVAILABLE = True
except ImportError:
    EXERCISE_AVAILABLE = False

# Import other modules with fallbacks
try:
    from chatbot import chat_ui
except Exception:
    def chat_ui():
        st.header("🤖 AI Assistant")
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        if prompt := st.chat_input("Ask about fitness..."):
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            response = "Try our specialized tools for personalized guidance!"
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            if AUTH_AVAILABLE and st.session_state.get('authenticated'):
                db = FitnessDatabase()
                db.save_mental_health_session(st.session_state.user['user_id'], {"chat": prompt, "response": response})
            st.rerun()

# Import authentication and health data systems
try:
    import pymongo
    import hashlib
    import uuid
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.graph_objects as go
    from dotenv import load_dotenv
    import random
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    load_dotenv()
    AUTH_AVAILABLE = True
except Exception:
    AUTH_AVAILABLE = False

# Email sending function
def send_password_reset_email(email, reset_token):
    try:
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        sender_email = os.getenv("EMAIL_ADDRESS")
        sender_password = os.getenv("EMAIL_PASSWORD")
        sender_name = os.getenv("EMAIL_FROM_NAME", "Forever Fit")
        
        if not sender_email or not sender_password:
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{sender_email}>"
        msg['To'] = email
        msg['Subject'] = "Password Reset - Forever Fit"
        
        # Email body
        body = f"""
        Hello,
        
        You requested a password reset for your Forever Fit account.
        
        Your password reset token is: {reset_token}
        
        This token will expire in 1 hour for security reasons.
        
        If you didn't request this reset, please ignore this email.
        
        Best regards,
        Forever Fit Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

try:
    from nutrition_ai_assistant import nutrition_ai_assistant_ui
    NUTRITION_AI_AVAILABLE = True
except Exception:
    NUTRITION_AI_AVAILABLE = False
    def nutrition_ai_assistant_ui():
        st.error("Nutrition AI Assistant not available")

try:
    from diet_planner import main as diet_planner_main
except Exception:
    def diet_planner_main():
        st.error("Advanced diet planner not available")
        st.info("Basic nutrition recommendations:")
        st.write("• Eat 5-6 small meals daily")
        st.write("• Include protein in every meal")
        st.write("• Stay hydrated with 8+ glasses water")

try:
    from mental_health_chatbot import mental_health_ui
except Exception:
    def mental_health_ui():
        st.header("🧠 Mental Health Support")
        mood = st.selectbox("How are you feeling?", ["Great", "Good", "Okay", "Not great", "Struggling"])
        stress = st.slider("Stress level", 1, 10, 5)
        if st.button("Save Check-in"):
            if AUTH_AVAILABLE and st.session_state.get('authenticated'):
                db = FitnessDatabase()
                db.save_mental_health_session(st.session_state.user['user_id'], {"mood": mood, "stress_level": stress})
                st.success("Check-in saved!")
            else:
                st.success("Check-in recorded!")

# Import advanced workout planner components
try:
    from advanced_workout_planner import (
        WorkoutRecommendationEngine, 
        PersonalizedWorkoutGenerator, 
        advanced_workout_planner_ui,
        display_workout_plan,
        generate_pdf_plan,
        generate_document_plan
    )
    ADVANCED_PLANNER_AVAILABLE = True
except ImportError:
    ADVANCED_PLANNER_AVAILABLE = False

def smart_workout_ui():
    if ADVANCED_PLANNER_AVAILABLE:
        advanced_workout_planner_ui()
    else:
        st.error("Advanced planner unavailable - missing dependencies")
        st.header("🏋️ Basic Workout Planner")
        
        goal = st.selectbox("Primary Goal", ["Build Muscle", "Lose Weight", "Improve Endurance", "General Fitness"])
        days = st.slider("Days per week", 2, 6, 3)
        
        if st.button("Generate Plan", type="primary"):
            st.success("Basic workout plan generated!")
            exercises = ["Push-ups", "Squats", "Planks", "Lunges", "Burpees"]
            for i, ex in enumerate(exercises, 1):
                st.write(f"{i}. **{ex}** - 3 sets x 12 reps")

# Import Health Integration Modules
try:
    from health_data_integration import health_data_input_ui, legendary_health_analytics, HealthDataManager
    from google_fit_integration import google_fit_integration_ui
    HEALTH_INTEGRATION_AVAILABLE = True
    print("✅ Health integration modules loaded successfully")
except ImportError as e:
    print(f"❌ Health integration import failed: {e}")
    HEALTH_INTEGRATION_AVAILABLE = False

# Import Authentication System
try:
    from auth_system import AuthenticationUI, FitnessDatabase as AuthFitnessDatabase
    AUTH_SYSTEM_AVAILABLE = True
    print("✅ Auth system loaded successfully")
except ImportError as e:
    print(f"❌ Auth system import failed: {e}")
    AUTH_SYSTEM_AVAILABLE = False
except Exception as e:
    print(f"❌ Auth system error: {e}")
    AUTH_SYSTEM_AVAILABLE = False

print(f"DEBUG: AUTH_AVAILABLE={AUTH_AVAILABLE}, AUTH_SYSTEM_AVAILABLE={AUTH_SYSTEM_AVAILABLE}")


# Integrated Authentication and Health Data Classes
class FitnessDatabase:
    def __init__(self):
        if AUTH_AVAILABLE:
            connection_string = os.getenv("MONGODB_CONNECTION_STRING")
            database_name = os.getenv("MONGODB_DATABASE", "fitness_ai")
            
            # Configure MongoDB client with multiple connection attempts
            connection_attempts = [
                # Attempt 1: Standard TLS connection
                {
                    "params": {
                        "tls": True,
                        "tlsInsecure": True,
                        "tlsAllowInvalidCertificates": True,
                        "tlsAllowInvalidHostnames": True,
                        "serverSelectionTimeoutMS": 8000,
                        "connectTimeoutMS": 8000,
                        "socketTimeoutMS": 8000,
                        "maxPoolSize": 5,
                        "retryWrites": True
                    },
                    "name": "TLS connection"
                },
                # Attempt 2: SSL connection
                {
                    "params": {
                        "ssl": True,
                        "ssl_cert_reqs": None,
                        "serverSelectionTimeoutMS": 5000,
                        "connectTimeoutMS": 5000,
                        "socketTimeoutMS": 5000
                    },
                    "name": "SSL connection"
                },
                # Attempt 3: Basic connection
                {
                    "params": {
                        "serverSelectionTimeoutMS": 3000,
                        "connectTimeoutMS": 3000
                    },
                    "name": "Basic connection"
                }
            ]
            
            self.client = None
            self.db = None
            
            for attempt in connection_attempts:
                try:
                    print(f"Trying MongoDB {attempt['name']}...")
                    self.client = pymongo.MongoClient(connection_string, **attempt['params'])
                    # Test connection
                    self.client.admin.command('ping')
                    self.db = self.client[database_name]
                    print(f"MongoDB connection successful with {attempt['name']}!")
                    break
                except Exception as e:
                    print(f"MongoDB {attempt['name']} failed: {str(e)[:100]}")
                    self.client = None
                    self.db = None
                    continue
            
            if not self.client:
                print("All MongoDB connection attempts failed. Running in offline mode.")
                return
            
            # Initialize collections only if database connection is successful
            if self.client and self.db is not None:
                self.users = self.db["users"]
                self.workouts = self.db["workouts"]
                self.diet_plans = self.db["diet_plans"]
                self.chat_history = self.db["chat_history"]
                self.daily_logs = self.db["daily_logs"]
                self.streaks = self.db["streaks"]
                self.health_data = self.db["health_data"]
                self.heart_rate = self.db["heart_rate"]
                self.steps = self.db["steps"]
                self.calories = self.db["calories"]
                self.sleep = self.db["sleep"]
                self.activities = self.db["activities"]
                
                # New collections
                self.voice_trainer_sessions = self.db["voice_trainer_sessions"]
                self.diet_assessments = self.db["diet_assessments"]
                self.nutrition_logs = self.db["nutrition_logs"]
                self.workout_assessments = self.db["workout_assessments"]
                self.mental_health_sessions = self.db["mental_health_sessions"]
                self.password_resets = self.db["password_resets"]
    
    def create_user(self, user_data):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            if self.users.find_one({"email": user_data['email']}):
                return False
            
            hashed_password = hashlib.sha256(user_data['password'].encode('utf-8')).hexdigest()
            
            user_doc = {
                "user_id": str(uuid.uuid4()),
                "email": user_data['email'],
                "password": hashed_password,
                "name": user_data['name'],
                "age": user_data['age'],
                "weight": user_data['weight'],
                "height": user_data['height'],
                "gender": user_data['gender'],
                "primary_goal": user_data['goal'],
                "created_at": datetime.now(),
                "last_login": datetime.now()
            }
            
            self.users.insert_one(user_doc)
            return True
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return False
    
    def authenticate_user(self, email, password):
        if not AUTH_AVAILABLE or not self.client:
            return None
        try:
            user = self.users.find_one({"email": email})
            print(f"DEBUG: Login attempt for {email}")
            if user:
                print("DEBUG: User found in database")
                input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
                stored_hash = user['password']
                match = input_hash == stored_hash
                print(f"DEBUG: Password match: {match}")
                if match:
                    self.users.update_one(
                        {"email": email},
                        {"$set": {"last_login": datetime.now()}}
                    )
                    return user
            else:
                print("DEBUG: User NOT found in database")
            return None
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return None
    
    def save_health_data(self, user_id, data_type, data):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            collection = getattr(self, data_type)
            data["user_id"] = user_id
            data["timestamp"] = datetime.now()
            data["date"] = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            collection.insert_one(data)
            return True
        except Exception as e:
            st.error(f"Error saving {data_type}: {e}")
            return False
    
    def get_health_analytics(self, user_id, days=30):
        if not AUTH_AVAILABLE or not self.client:
            return {}
        try:
            from datetime import timedelta
            start_date = datetime.now() - timedelta(days=days)
            
            return {
                "heart_rate": list(self.heart_rate.find({"user_id": user_id, "date": {"$gte": start_date}}).sort("timestamp", 1)),
                "steps": list(self.steps.find({"user_id": user_id, "date": {"$gte": start_date}}).sort("date", 1)),
                "calories": list(self.calories.find({"user_id": user_id, "date": {"$gte": start_date}}).sort("date", 1)),
                "sleep": list(self.sleep.find({"user_id": user_id, "date": {"$gte": start_date}}).sort("date", 1)),
                "activities": list(self.activities.find({"user_id": user_id, "date": {"$gte": start_date}}).sort("timestamp", 1))
            }
        except Exception as e:
            st.error(f"Error fetching analytics: {e}")
            return {}
    
    def save_voice_session(self, user_id, session_data):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            session_data["user_id"] = user_id
            session_data["timestamp"] = datetime.now()
            self.voice_trainer_sessions.insert_one(session_data)
            return True
        except Exception:
            return False
    
    def save_diet_assessment(self, user_id, responses, plan):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            self.diet_assessments.insert_one({
                "user_id": user_id,
                "responses": responses,
                "generated_plan": plan,
                "timestamp": datetime.now()
            })
            return True
        except Exception:
            return False
    
    def save_nutrition_log(self, user_id, log_data):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            log_data["user_id"] = user_id
            log_data["timestamp"] = datetime.now()
            self.nutrition_logs.insert_one(log_data)
            return True
        except Exception:
            return False
    
    def save_workout_assessment(self, user_id, responses, plan):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            self.workout_assessments.insert_one({
                "user_id": user_id,
                "responses": responses,
                "generated_plan": plan,
                "timestamp": datetime.now()
            })
            return True
        except Exception:
            return False
    
    def save_mental_health_session(self, user_id, session_data):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            session_data["user_id"] = user_id
            session_data["timestamp"] = datetime.now()
            self.mental_health_sessions.insert_one(session_data)
            return True
        except Exception:
            return False
    
    def get_user_data(self, user_id):
        if not AUTH_AVAILABLE or not self.client:
            return {}
        try:
            user = self.users.find_one({"user_id": user_id})
            return {
                "user": user,
                "workout_plans": list(self.workout_assessments.find({"user_id": user_id}).sort("timestamp", -1).limit(5)),
                "diet_plans": list(self.diet_assessments.find({"user_id": user_id}).sort("timestamp", -1).limit(5)),
                "nutrition_logs": list(self.nutrition_logs.find({"user_id": user_id}).sort("timestamp", -1).limit(10)),
                "voice_sessions": list(self.voice_trainer_sessions.find({"user_id": user_id}).sort("timestamp", -1).limit(10)),
                "mental_health_sessions": list(self.mental_health_sessions.find({"user_id": user_id}).sort("timestamp", -1).limit(5)),
                "chat_history": [],
                "daily_logs": [],
                "streak": {"current_streak": 0, "max_streak": 0}
            }
        except Exception:
            return {}
    
    def create_password_reset_token(self, email):
        if not AUTH_AVAILABLE or not self.client:
            return None
        try:
            user = self.users.find_one({"email": email})
            if not user:
                return None
            
            # Generate reset token
            reset_token = str(uuid.uuid4())
            expires_at = datetime.now() + timedelta(hours=1)  # Token expires in 1 hour
            
            # Save reset token
            self.password_resets.insert_one({
                "email": email,
                "token": reset_token,
                "expires_at": expires_at,
                "used": False,
                "created_at": datetime.now()
            })
            
            return reset_token
        except Exception as e:
            print(f"Error creating reset token: {e}")
            return None
    
    def verify_reset_token(self, token):
        if not AUTH_AVAILABLE or not self.client:
            return None
        try:
            reset_request = self.password_resets.find_one({
                "token": token,
                "used": False,
                "expires_at": {"$gt": datetime.now()}
            })
            return reset_request
        except Exception:
            return None
    
    def reset_password(self, token, new_password):
        if not AUTH_AVAILABLE or not self.client:
            return False
        try:
            reset_request = self.verify_reset_token(token)
            if not reset_request:
                return False
            
            # Hash new password
            hashed_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
            
            # Update user password
            self.users.update_one(
                {"email": reset_request["email"]},
                {"$set": {"password": hashed_password, "updated_at": datetime.now()}}
            )
            
            # Mark token as used
            self.password_resets.update_one(
                {"token": token},
                {"$set": {"used": True, "used_at": datetime.now()}}
            )
            
            return True
        except Exception as e:
            print(f"Error resetting password: {e}")
            return False

class AuthenticationUI:
    def __init__(self):
        if AUTH_AVAILABLE:
            self.db = FitnessDatabase()
        else:
            self.db = None
    
    def show_forgot_password(self):
        st.subheader("🔐 Forgot Password")
        
        if "reset_step" not in st.session_state:
            st.session_state.reset_step = "email"
        
        if st.session_state.reset_step == "email":
            with st.form("forgot_password_form"):
                st.write("Enter your email address to receive a password reset token:")
                email = st.text_input("Email Address")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Send Reset Token", type="primary"):
                        if email:
                            if self.db and self.db.client:
                                reset_token = self.db.create_password_reset_token(email)
                                if reset_token:
                                    if send_password_reset_email(email, reset_token):
                                        st.success("Password reset token sent to your email!")
                                        st.session_state.reset_step = "token"
                                        st.session_state.reset_email = email
                                        st.rerun()
                                    else:
                                        st.error("Failed to send email. Please check email configuration.")
                                        st.info(f"Your reset token is: {reset_token}")
                                        st.session_state.reset_step = "token"
                                        st.session_state.reset_email = email
                                        st.session_state.manual_token = reset_token
                                else:
                                    st.error("Email not found in our system.")
                            else:
                                st.error("Database connection unavailable.")
                        else:
                            st.error("Please enter your email address.")
                
                with col2:
                    if st.form_submit_button("Back to Login"):
                        st.session_state.reset_step = "email"
                        st.rerun()
        
        elif st.session_state.reset_step == "token":
            with st.form("reset_password_form"):
                st.write(f"Enter the reset token sent to {st.session_state.get('reset_email', 'your email')}:")
                token = st.text_input("Reset Token")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Reset Password", type="primary"):
                        if token and new_password and confirm_password:
                            if new_password != confirm_password:
                                st.error("Passwords do not match.")
                            elif len(new_password) < 6:
                                st.error("Password must be at least 6 characters long.")
                            else:
                                if self.db and self.db.client:
                                    if self.db.reset_password(token, new_password):
                                        st.success("Password reset successfully! You can now login with your new password.")
                                        st.session_state.reset_step = "email"
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.error("Invalid or expired reset token.")
                                else:
                                    st.error("Database connection unavailable.")
                        else:
                            st.error("Please fill all fields.")
                
                with col2:
                    if st.form_submit_button("Back to Email"):
                        st.session_state.reset_step = "email"
                        st.rerun()
    
    def show_login_page(self):
        if not AUTH_AVAILABLE:
            st.error("Authentication system not available")
            return
        
        # Check if MongoDB is available
        db_available = hasattr(self, 'db') and self.db and hasattr(self.db, 'client') and self.db.client
        if not db_available:
            st.warning("⚠️ Database connection unavailable")
            st.info("You can still use the application with limited features")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Continue as Guest", type="primary"):
                    st.session_state.user = {"name": "Guest User", "user_id": "guest"}
                    st.session_state.authenticated = True
                    st.success("Continuing as guest user")
                    st.rerun()
            
            with col2:
                if st.button("Retry Connection"):
                    # Try to reinitialize database connection
                    self.db = FitnessDatabase()
                    st.rerun()
            
            st.divider()
            st.subheader("Database Connection Issues")
            st.write("**Possible solutions:**")
            st.write("• Check your internet connection")
            st.write("• Verify MongoDB connection string in .env file")
            st.write("• Ensure MongoDB Atlas cluster is running")
            st.write("• Check firewall settings")
            return
            
        render_legendary_header()
        
        tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
        
        with tab1:
            with card_container():
                with st.form("login_form"):
                    st.subheader("Welcome Back!")
                    email = st.text_input("Email")
                    password = st.text_input("Password", type="password")
                    
                    if st.form_submit_button("Login", type="primary"):
                        if email and password:
                            user = self.db.authenticate_user(email, password)
                            if user:
                                st.session_state.user = user
                                st.session_state.authenticated = True
                                st.success("Login successful!")
                                st.rerun()
                            else:
                                st.error("Invalid credentials")
                        else:
                            st.error("Please fill all fields")
        
        with tab2:
            with card_container():
                with st.form("signup_form"):
                    st.subheader("Create Account")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Full Name")
                        email = st.text_input("Email")
                        password = st.text_input("Password", type="password")
                    
                    with col2:
                        age = st.number_input("Age", min_value=16, max_value=80, value=25)
                        weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
                        height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
                    
                    gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
                    goal = st.selectbox("Primary Goal", [
                        "Lose weight", "Build muscle", "Improve endurance", 
                        "General fitness", "Strength training"
                    ])
                    
                    if st.form_submit_button("Create Account", type="primary"):
                        if all([name, email, password, age, weight, height]):
                            user_data = {
                                "name": name, "email": email, "password": password,
                                "age": age, "weight": weight, "height": height,
                                "gender": gender, "goal": goal
                            }
                            
                            if self.db and self.db.client:
                                if self.db.create_user(user_data):
                                    st.success("Account created successfully! Please login.")
                                else:
                                    st.error("Email already exists or error creating account")
                            else:
                                st.error("Database connection unavailable. Running in offline mode.")
                        else:
                            st.error("Please fill all fields")
        
        with tab3:
            with card_container():
                self.show_forgot_password()

# Check if mediapipe is available
MEDIAPIPE_AVAILABLE = False
mp = None
try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
    print("MediaPipe successfully imported!")
except Exception as e:
    print(f"MediaPipe import failed: {e}")
    try:
        # Try alternative import
        import mediapipe
        mp = mediapipe
        MEDIAPIPE_AVAILABLE = True
        print("MediaPipe imported via alternative method!")
    except:
        MEDIAPIPE_AVAILABLE = False
        mp = None

# Initialize ElevenLabs with new API
ELEVENLABS_AVAILABLE = False
try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if api_key:
        client = ElevenLabs(api_key=api_key)
        ELEVENLABS_AVAILABLE = True
except:
    try:
        # Fallback to older API
        from elevenlabs import generate, stream, set_api_key

        api_key = os.getenv("ELEVENLABS_API_KEY")
        if api_key:
            set_api_key(api_key)
            ELEVENLABS_AVAILABLE = True
    except:
        pass


# Voice Trainer Class
class VoiceTrainer:
    def __init__(self):
        self.mp_pose = None
        self.pose = None
        self.mp_drawing = None
        self.last_voice_time = 0
        self.basic_mode = False # New flag
        
        # Try to initialize MediaPipe
        try:
            import mediapipe as mp
            self.mp_pose = mp.solutions.pose
            self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
            self.mp_drawing = mp.solutions.drawing_utils
            print("VoiceTrainer: MediaPipe initialized successfully")
            global MEDIAPIPE_AVAILABLE
            MEDIAPIPE_AVAILABLE = True
        except Exception as e:
            print(f"VoiceTrainer: MediaPipe initialization failed: {e}")
            self.mp_pose = None
            self.pose = None
            self.mp_drawing = None
            MEDIAPIPE_AVAILABLE = False
            self.basic_mode = True # Set basic_mode to True if MediaPipe fails

    def speak(self, text):
        if not ELEVENLABS_AVAILABLE or time.time() - self.last_voice_time < 3:
            return
        try:
            # Try new API first
            if "client" in globals():
                audio = client.generate(
                    text=text, voice="Arnold", model="eleven_monolingual_v1"
                )
                threading.Thread(target=lambda: play(audio), daemon=True).start()
            else:
                # Fallback to old API
                audio = generate(
                    text=text, voice="Arnold", model="eleven_monolingual_v1"
                )
                threading.Thread(target=lambda: stream(audio), daemon=True).start()

            self.last_voice_time = time.time()
        except Exception as e:
            print(f"Voice error: {e}")

    def analyze_form_and_count_reps(self, landmarks, exercise, current_stage, rep_counter, frame_history=[]):
        if len(landmarks) < 33:
            return {"score": 0, "feedback": "No pose detected", "stage": current_stage, "reps": rep_counter, "form_correct": False, "confidence": 0}

        form_correct = True
        feedback = "Good form!"
        score = 100
        new_stage = current_stage
        new_reps = rep_counter
        confidence = 0
        
        # Store last 10 frames for smoothing
        if len(frame_history) > 10:
            frame_history.pop(0)
        frame_history.append(landmarks)

        if exercise == "bicep_curl":
            # Get both arms for better accuracy
            right_shoulder = [landmarks[12].x, landmarks[12].y]
            right_elbow = [landmarks[14].x, landmarks[14].y] 
            right_wrist = [landmarks[16].x, landmarks[16].y]
            
            left_shoulder = [landmarks[11].x, landmarks[11].y]
            left_elbow = [landmarks[13].x, landmarks[13].y]
            left_wrist = [landmarks[15].x, landmarks[15].y]
            
            # Calculate angles for both arms
            right_angle = self.calculate_angle(right_shoulder, right_elbow, right_wrist)
            left_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            # Use the arm with better visibility (higher confidence)
            if abs(right_wrist[0] - right_elbow[0]) > abs(left_wrist[0] - left_elbow[0]):
                primary_angle = right_angle
                primary_arm = "right"
            else:
                primary_angle = left_angle
                primary_arm = "left"
            
            # Advanced form checking
            form_issues = []
            
            # Check elbow stability
            if primary_arm == "right":
                elbow_drift = abs(right_elbow[0] - right_shoulder[0])
            else:
                elbow_drift = abs(left_elbow[0] - left_shoulder[0])
                
            if elbow_drift > 0.15:
                form_issues.append("Keep elbow stable!")
                score -= 20
            
            # Check range of motion
            if primary_angle < 40 or primary_angle > 165:
                form_issues.append("Invalid arm position!")
                score -= 30
            
            # Calculate movement confidence using frame history
            if len(frame_history) >= 3:
                angle_changes = []
                for i in range(len(frame_history)-2):
                    prev_angle = self.calculate_angle(
                        [frame_history[i][12].x, frame_history[i][12].y],
                        [frame_history[i][14].x, frame_history[i][14].y],
                        [frame_history[i][16].x, frame_history[i][16].y]
                    )
                    curr_angle = self.calculate_angle(
                        [frame_history[i+1][12].x, frame_history[i+1][12].y],
                        [frame_history[i+1][14].x, frame_history[i+1][14].y],
                        [frame_history[i+1][16].x, frame_history[i+1][16].y]
                    )
                    angle_changes.append(abs(curr_angle - prev_angle))
                
                avg_change = sum(angle_changes) / len(angle_changes)
                confidence = min(100, avg_change * 5)  # Movement confidence
            
            form_correct = len(form_issues) == 0 and confidence > 20
            
            if form_issues:
                feedback = " | ".join(form_issues)
                score = max(20, score)
            
            # Enhanced rep counting with confidence threshold
            if form_correct and confidence > 30:
                motivational_messages = [
                    "🔥 FIRE! Biceps blazing!", "💪 BEAST MODE! Unstoppable!", "⚡ LIGHTNING! Pure power!",
                    "🎯 PRECISION! Perfect form!", "💥 EXPLOSIVE! Keep crushing!", "✨ FLAWLESS! You're a machine!"
                ]
                
                # Simplified rep counting - check for complete range of motion
                if hasattr(st.session_state, 'last_angle'):
                    angle_diff = abs(primary_angle - st.session_state.last_angle)
                    
                    # Check if user completed full range (from extended to curled and back)
                    if (st.session_state.last_angle > 130 and primary_angle < 80) or \
                       (st.session_state.last_angle < 80 and primary_angle > 130):
                        if angle_diff > 50 and confidence > 40:  # Significant movement
                            new_reps += 1
                            if new_reps > 15:
                                feedback = f"EXCELLENT! {new_reps} reps completed! Time to rest!"
                                self.speak(f"Outstanding! {new_reps} perfect reps! Take a break!")
                            else:
                                msg = motivational_messages[new_reps % len(motivational_messages)]
                                feedback = f"{msg} Rep {new_reps} completed!"
                                self.speak(f"Perfect rep! That's {new_reps}!")
                
                # Store current angle for next comparison
                st.session_state.last_angle = primary_angle
                
                # Simple feedback based on current position
                if primary_angle > 130:
                    feedback = "Arms extended - Good starting position!"
                elif primary_angle < 80:
                    feedback = "Full contraction - Excellent squeeze!"
                else:
                    feedback = "Keep moving through full range of motion!"
            
            elif not form_correct:
                feedback = f"❌ {feedback} - Fix form to count reps!"
                score = max(10, score)
            else:
                feedback = "🔄 Move your arm more to register motion!"

        elif exercise == "push_up":
            # Get key landmarks
            left_shoulder = [landmarks[11].x, landmarks[11].y]
            left_elbow = [landmarks[13].x, landmarks[13].y]
            left_wrist = [landmarks[15].x, landmarks[15].y]
            left_hip = [landmarks[23].x, landmarks[23].y]
            left_knee = [landmarks[25].x, landmarks[25].y]
            
            # Calculate angles
            elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            body_angle = self.calculate_angle(left_shoulder, left_hip, left_knee)
            
            # Check form
            if body_angle < 160:  # Body not straight
                form_correct = False
                feedback = "Keep your body straight like a plank!"
                score = 30
                self.speak("Straighten your body, maintain plank position")
                
            elif form_correct:
                power_messages = [
                    "Warrior strength! 🗡️", "Titanium core! 🛡️", "Explosive power! 💥",
                    "Steel determination! ⚔️", "Unstoppable! 🚀", "Champion form! 👑"
                ]
                
                if elbow_angle > 160:  # Arms extended (up position)
                    if current_stage == "down":
                        new_reps += 1
                        if new_reps > 15:
                            feedback = f"🛑 PHENOMENAL! {new_reps} push-ups! REST TIME! 🛑"
                            self.speak(f"Outstanding! {new_reps} perfect push-ups! Time to rest and recover!")
                        else:
                            msg = power_messages[new_reps % len(power_messages)]
                            feedback = f"{msg} Push-up {new_reps} CRUSHED!"
                            self.speak(f"Powerful push-up! Number {new_reps} completed!")
                    new_stage = "up"
                    if new_reps <= 15:
                        feedback = "Locked and loaded! Drop it down! 💪"
                    
                elif elbow_angle < 90:  # Arms bent (down position)
                    new_stage = "down"
                    feedback = "Perfect depth! Explode up! 🚀"
                    
                else:
                    if current_stage == "up":
                        feedback = "Chest to the floor! No mercy! 🔥"
                    else:
                        feedback = "Drive through! Pure strength! ⚡"

        elif exercise == "squat":
            # Get key landmarks
            left_hip = [landmarks[23].x, landmarks[23].y]
            left_knee = [landmarks[25].x, landmarks[25].y]
            left_ankle = [landmarks[27].x, landmarks[27].y]
            left_shoulder = [landmarks[11].x, landmarks[11].y]
            
            # Calculate angles
            knee_angle = self.calculate_angle(left_hip, left_knee, left_ankle)
            
            # Check if knees go past toes (form check)
            if left_knee[0] > left_ankle[0] + 0.05:  # Knee too far forward
                form_correct = False
                feedback = "Don't let your knees go past your toes!"
                score = 35
                self.speak("Keep your knees behind your toes, sit back more")
                
            elif form_correct:
                squat_power = [
                    "Thunder thighs! ⚡", "Leg day legend! 🦵", "Squat monster! 👹",
                    "Glute power! 🍑", "Quad crusher! 💥", "Lower body beast! 🔥"
                ]
                
                if knee_angle > 160:  # Standing position
                    if current_stage == "down":
                        new_reps += 1
                        if new_reps > 15:
                            feedback = f"🛑 LEGENDARY! {new_reps} squats! RECOVERY TIME! 🛑"
                            self.speak(f"Incredible! {new_reps} perfect squats! Your legs need rest now!")
                        else:
                            msg = squat_power[new_reps % len(squat_power)]
                            feedback = f"{msg} Squat {new_reps} DOMINATED!"
                            self.speak(f"Fantastic squat! That's {new_reps}! Keep dominating!")
                    new_stage = "up"
                    if new_reps <= 15:
                        feedback = "Standing strong! Drop it low! 💪"
                    
                elif knee_angle < 100:  # Squat position
                    new_stage = "down"
                    feedback = "Deep and powerful! Rise up! 🚀"
                    
                else:
                    if current_stage == "up":
                        feedback = "Sit back! Feel the burn! 🔥"
                    else:
                        feedback = "Power up! Legs of steel! ⚡"

        elif exercise == "shoulder_press":
            # Get key landmarks
            left_shoulder = [landmarks[11].x, landmarks[11].y]
            left_elbow = [landmarks[13].x, landmarks[13].y]
            left_wrist = [landmarks[15].x, landmarks[15].y]
            
            # Calculate angle
            elbow_angle = self.calculate_angle(left_shoulder, left_elbow, left_wrist)
            
            # Check form - wrists should be above elbows
            if left_wrist[1] > left_elbow[1]:  # Wrist below elbow (bad form)
                form_correct = False
                feedback = "Keep your wrists above your elbows!"
                score = 45
                self.speak("Lift your hands higher, wrists above elbows")
                
            elif form_correct:
                shoulder_fire = [
                    "Shoulder cannon! 💥", "Press machine! 🤖", "Overhead beast! 🦍",
                    "Deltoid destroyer! 🔥", "Sky crusher! ☁️", "Press master! 👑"
                ]
                
                if elbow_angle > 160:  # Arms extended overhead
                    if current_stage == "down":
                        new_reps += 1
                        if new_reps > 15:
                            feedback = f"🛑 INCREDIBLE! {new_reps} presses! TIME TO REST! 🛑"
                            self.speak(f"Amazing! {new_reps} perfect presses! Rest those shoulders now!")
                        else:
                            msg = shoulder_fire[new_reps % len(shoulder_fire)]
                            feedback = f"{msg} Press {new_reps} CONQUERED!"
                            self.speak(f"Excellent press! Number {new_reps} completed!")
                    new_stage = "up"
                    if new_reps <= 15:
                        feedback = "Locked out! Bring it down! 💪"
                    
                elif elbow_angle < 90:  # Arms at shoulder level
                    new_stage = "down"
                    feedback = "Perfect position! Press to the sky! 🚀"
                    
                else:
                    if current_stage == "down":
                        feedback = "Drive it up! Shoulder power! ⚡"
                    else:
                        feedback = "Control the descent! Pure strength! 🔥"

        return {
            "score": score,
            "feedback": feedback,
            "stage": new_stage,
            "reps": new_reps,
            "form_correct": form_correct,
            "confidence": confidence,
            "primary_angle": primary_angle if exercise == "bicep_curl" else 0
        }

    def calculate_angle(self, p1, p2, p3):
        v1 = np.array(p1) - np.array(p2)
        v2 = np.array(p3) - np.array(p2)
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.degrees(np.arccos(np.clip(cos_angle, -1.0, 1.0)))

# Local health functions removed in favor of external modules



def voice_trainer_ui():
    """Voice trainer interface with professional UI."""
    st.header("Voice-Guided Exercise Trainer")
    st.caption("Real-time form correction with AI voice feedback")
    
    # Information panel
    with st.container():
        st.info(
            "**Form-First Training**: Repetitions are only counted when proper form is maintained. "
            "The system provides real-time guidance to perfect your technique."
        )

    # System requirements check
    if not ELEVENLABS_AVAILABLE:
        st.warning(
            "**ElevenLabs API Key Missing**: Voice feedback will be disabled. "
            "Please set `ELEVENLABS_API_KEY` in your `.env` file for full experience."
        )
    
    # Check for MediaPipe availability or Basic Mode
    if not MEDIAPIPE_AVAILABLE:
        st.warning(
            "**MediaPipe Unavailable**: Real-time pose detection and form correction are disabled. "
            "The Voice Trainer will run in basic mode. Ensure MediaPipe is installed correctly."
        )
    elif st.session_state.get('voice_trainer') and st.session_state.voice_trainer.basic_mode:
        st.info(
            "**Basic Mode Active**: MediaPipe initialization failed. "
            "Running in basic mode without pose detection. Voice feedback is still available."
        )
    
    # Try to initialize trainer even if global check failed
    if "voice_trainer" not in st.session_state:
        st.session_state.voice_trainer = VoiceTrainer()
    
    trainer = st.session_state.voice_trainer
    
    if not trainer.pose:
        st.warning("MediaPipe pose detection not available. Using basic exercise mode.")
        st.info("💡 Try restarting the application or check MediaPipe installation.")
        
        # Provide basic exercise guidance without pose detection
        st.subheader("🎤 Basic Exercise Mode")
        exercise = st.selectbox("Select Exercise:", ["Push Up", "Squat", "Bicep Curl", "Shoulder Press"])
        
        if st.button("Start Basic Training", type="primary"):
            st.success(f"Starting {exercise} training in basic mode!")
            st.info("Count your own reps and focus on proper form:")
            
            # Basic exercise instructions
            if exercise == "Push Up":
                st.write("• Keep body straight like a plank")
                st.write("• Lower chest to floor, push back up")
                st.write("• Don't let hips sag or pike up")
            elif exercise == "Squat":
                st.write("• Feet shoulder-width apart")
                st.write("• Sit back like sitting in a chair")
                st.write("• Keep knees behind toes")
            elif exercise == "Bicep Curl":
                st.write("• Keep elbows at your sides")
                st.write("• Curl weight up, squeeze at top")
                st.write("• Lower with control")
            elif exercise == "Shoulder Press":
                st.write("• Press weight straight overhead")
                st.write("• Keep core tight")
                st.write("• Don't arch your back")
        
        return

    # trainer is already initialized above
    # Continue with full pose detection mode

    col1, col2 = st.columns(2)

    with col1:
        exercise = st.selectbox(
            "Select Exercise:",
            ["Push Up", "Squat", "Bicep Curl", "Shoulder Press"],
            key="voice_exercise",
        )

        col1a, col1b = st.columns(2)
        with col1a:
            if st.button("Start Training", key="start_voice", type="primary"):
                # Reset counters when starting
                st.session_state.rep_count = 0
                st.session_state.last_angle = 0
                st.session_state.last_saved_reps = 0
                if ELEVENLABS_AVAILABLE:
                    trainer.speak(f"Starting {exercise} with voice feedback. Remember, only perfect form counts!")
                    st.success("Training session initiated with voice guidance")
                else:
                    st.success("Training session initiated with visual feedback")
        
        with col1b:
            if st.button("Reset Counter", key="reset_reps"):
                st.session_state.rep_count = 0
                st.session_state.last_angle = 0
                st.success("Repetition counter reset")

    with col2:
        camera_enabled = st.checkbox("Enable Camera Feed", key="voice_camera")
        
        # Display current metrics
        if "rep_count" in st.session_state:
            st.metric("Repetitions Completed", st.session_state.rep_count)

    if camera_enabled:
        st.subheader("Live Training Session")
        st.caption("Real-time form analysis and feedback")

        video_col, metrics_col = st.columns([3, 1])

        with video_col:
            stframe = st.empty()

        with metrics_col:
            metrics_placeholder = st.empty()

        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Camera access unavailable. Please check camera permissions.")
            return

        frame_count = 0

        # Initialize session state for rep counting
        if "rep_count" not in st.session_state:
            st.session_state.rep_count = 0
        if "last_feedback_time" not in st.session_state:
            st.session_state.last_feedback_time = 0
        if "form_correction_count" not in st.session_state:
            st.session_state.form_correction_count = 0
        if "frame_history" not in st.session_state:
            st.session_state.frame_history = []
        if "last_angle" not in st.session_state:
            st.session_state.last_angle = 0

        while camera_enabled:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % 2 == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = trainer.pose.process(rgb_frame)
                frame = cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR)

                if results.pose_landmarks:
                    trainer.mp_drawing.draw_landmarks(
                        frame, results.pose_landmarks, trainer.mp_pose.POSE_CONNECTIONS
                    )

                    # Analyze form and count reps with frame history
                    analysis = trainer.analyze_form_and_count_reps(
                        results.pose_landmarks.landmark,
                        exercise.lower().replace(" ", "_"),
                        None,  # No longer using exercise_stage
                        st.session_state.rep_count,
                        st.session_state.frame_history
                    )
                    
                    # Update session state
                    st.session_state.rep_count = analysis["reps"]
                    
                    # Save session data
                    if AUTH_AVAILABLE and st.session_state.get('authenticated') and analysis["reps"] > 0:
                        if "last_saved_reps" not in st.session_state:
                            st.session_state.last_saved_reps = 0
                        if analysis["reps"] - st.session_state.last_saved_reps >= 5:
                            db = FitnessDatabase()
                            session_data = {
                                "exercise_type": exercise.lower().replace(" ", "_"),
                                "total_reps": analysis["reps"],
                                "form_score": analysis["score"]
                            }
                            db.save_voice_session(st.session_state.user['user_id'], session_data)
                            st.session_state.last_saved_reps = analysis["reps"]

                    # Visual feedback overlay
                    score = analysis["score"]
                    form_correct = analysis["form_correct"]
                    
                    # Form status indicator with progress bar
                    form_color = (0, 255, 0) if form_correct else (0, 0, 255)
                    form_text = "CORRECT FORM" if form_correct else "INCORRECT FORM - FIX TO COUNT REP"
                    
                    # Background for form status
                    cv2.rectangle(frame, (10, 10), (600, 50), (0, 0, 0), -1)
                    cv2.putText(
                        frame,
                        form_text,
                        (15, 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        form_color,
                        2,
                    )
                    
                    # Dual progress bars - Form Quality and Movement Confidence
                    form_bar_width = int(300 * (score / 100))
                    confidence_bar_width = int(300 * (analysis.get('confidence', 0) / 100))
                    
                    # Form quality bar
                    cv2.rectangle(frame, (10, 60), (310, 75), (50, 50, 50), -1)
                    cv2.rectangle(frame, (10, 60), (10 + form_bar_width, 75), form_color, -1)
                    cv2.putText(frame, f"Form: {score}%", (320, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Movement confidence bar
                    cv2.rectangle(frame, (10, 80), (310, 95), (50, 50, 50), -1)
                    cv2.rectangle(frame, (10, 80), (10 + confidence_bar_width, 95), (0, 255, 255), -1)
                    cv2.putText(frame, f"Motion: {int(analysis.get('confidence', 0))}%", (320, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                    # Enhanced rep counter with pulsing effect for new reps
                    rep_color = (0, 255, 0) if analysis.get('confidence', 0) > 50 else (255, 255, 255)
                    cv2.putText(
                        frame,
                        f"REPS: {st.session_state.rep_count}",
                        (10, 115),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.2,
                        rep_color,
                        3,
                    )
                    
                    # Form status instead of stage
                    status_text = "CORRECT FORM" if form_correct else "ADJUST FORM"
                    status_color = (0, 255, 0) if form_correct else (0, 165, 255)
                    cv2.putText(
                        frame,
                        f"STATUS: {status_text}",
                        (10, 155),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        status_color,
                        2,
                    )
                    
                    # Enhanced feedback message with better formatting
                    feedback_text = analysis["feedback"]
                    if len(feedback_text) > 50:
                        # Split long feedback into multiple lines
                        words = feedback_text.split(" ")
                        lines = []
                        current_line = ""
                        for word in words:
                            if len(current_line + word) < 40:
                                current_line += word + " "
                            else:
                                lines.append(current_line.strip())
                                current_line = word + " "
                        if current_line:
                            lines.append(current_line.strip())
                    else:
                        lines = [feedback_text]
                    
                    for i, line in enumerate(lines[:3]):  # Max 3 lines
                        cv2.putText(
                            frame,
                            line,
                            (10, 195 + i * 25),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            form_color,
                            2,
                        )

                    # Exercise name with enhanced info
                    cv2.putText(
                        frame,
                        f"Exercise: {exercise} | AI Precision Mode",
                        (10, frame.shape[0] - 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2,
                    )
                    
                    # Show detailed info for bicep curl
                    if exercise.lower().replace(" ", "_") == "bicep_curl":
                        cv2.putText(
                            frame,
                            f"Angle: {int(analysis.get('primary_angle', 0))}° | Confidence: {int(analysis.get('confidence', 0))}%",
                            (10, frame.shape[0] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (0, 255, 255),
                            1,
                        )

                    # Metrics display
                    with metrics_placeholder.container():
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Repetitions", st.session_state.rep_count)
                            if form_correct:
                                st.success("Form: Excellent")
                            else:
                                st.error("Form: Needs Correction")
                        
                        with col2:
                            st.metric("Form Quality", f"{score}%")
                            if "confidence" in analysis:
                                st.metric("Movement Confidence", f"{int(analysis['confidence'])}%")
                            # Remove stage display - no longer needed
                        
                        # Clean feedback without emojis
                        feedback_clean = analysis['feedback'].replace('🔥', '').replace('💪', '').replace('⚡', '').replace('🎯', '').replace('💥', '').replace('✨', '').replace('🛑', '').replace('❌', '').replace('🔄', '')
                        
                        if st.session_state.rep_count > 15:
                            st.error(f"EXCELLENT WORK! {st.session_state.rep_count} repetitions completed!")
                            st.warning("Recommended rest period: 60-90 seconds")
                        elif form_correct:
                            st.success(feedback_clean)
                        else:
                            st.warning(feedback_clean)
                            st.error("Repetition will not count until form is corrected")

                        # System status
                        if ELEVENLABS_AVAILABLE:
                            st.info("Voice guidance: Active")
                        else:
                            st.info("Visual feedback: Active")

                else:
                    cv2.putText(
                        frame,
                        "Position yourself in camera view for pose detection",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 0, 255),
                        2,
                    )

                stframe.image(frame, channels="BGR", use_container_width=True)

            frame_count += 1

            if not st.session_state.get("voice_camera", False):
                break

        cap.release()


# Initialize exercise coach if available
exercise_coach = None
if MEDIAPIPE_AVAILABLE and EXERCISE_AVAILABLE:
    try:
        exercise_coach = ExerciseCoach()
    except Exception as e:
        st.error(f"Error initializing exercise coach: {e}")
        EXERCISE_AVAILABLE = False


def main():
    # Apply Legendary Styles immediately
    apply_legendary_styles()

    # Check authentication first - ALWAYS require login
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        # Show authentication status for debugging
        st.sidebar.info(f"Auth Available: {AUTH_AVAILABLE}")
        st.sidebar.info(f"Auth System Available: {AUTH_SYSTEM_AVAILABLE}")
        
        if AUTH_AVAILABLE and AUTH_SYSTEM_AVAILABLE:
            auth_ui = AuthenticationUI()
            auth_ui.show_login_page()
            return
        else:
            # Show error if auth system not available
            st.error("Authentication system not available. Please check dependencies.")
            st.info("Missing dependencies:")
            if not AUTH_AVAILABLE:
                st.write("- MongoDB connection libraries (pymongo, pandas, plotly)")
            if not AUTH_SYSTEM_AVAILABLE:
                st.write("- auth_system.py module")
            st.stop()
    else:
        # Get user data for authenticated user (only if not guest)
        if st.session_state.user.get('user_id') != 'guest':
            db = AuthFitnessDatabase()
            if db and db.client:
                user_data = db.get_user_data(st.session_state.user['user_id'])
            else:
                user_data = {}
    
    # Theme Toggle
    if "theme" not in st.session_state:
        st.session_state.theme = "Dark"
    
    with st.sidebar:
        st.header("⚙️ Settings")
        st.radio("Theme Mode", ["Light", "Dark"], key="theme")
        st.divider()

    # Apply Legendary Styles (re-apply to catch theme change)
    apply_legendary_styles()



    
    # Header Section with user info
    if AUTH_AVAILABLE and st.session_state.authenticated:
        col1, col2 = st.columns([3, 1])
        with col1:
            render_legendary_header()
            st.markdown(f'<p class="sub-header" style="margin-top: -2rem;">Welcome back, {st.session_state.user["name"]}! Ready to crush your fitness goals?</p>', unsafe_allow_html=True)
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("🚪 Logout", type="secondary"):
                st.session_state.clear()
                st.rerun()
    else:
        render_legendary_header()

    # Check DeepSeek availability
    DEEPSEEK_AVAILABLE = False
    try:
        from deepseek_reasoning import DeepSeekReasoningEngine, initialize_deepseek_reasoning
        deepseek_reasoning = initialize_deepseek_reasoning()
        DEEPSEEK_AVAILABLE = deepseek_reasoning is not None
    except ImportError:
        DEEPSEEK_AVAILABLE = False

    # Database connection status
    if AUTH_AVAILABLE:
        db_test = FitnessDatabase()
        db_connected = db_test and db_test.client is not None
    else:
        db_connected = False
    
    # System Status Dashboard
    st.markdown("### 🖥️ SYSTEM STATUS")
    
    with card_container():
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_status_badge(MEDIAPIPE_AVAILABLE, "MediaPipe")
        with col2:
            render_status_badge(ELEVENLABS_AVAILABLE, "Voice AI")
        with col3:
            render_status_badge(EXERCISE_AVAILABLE, "Exercise AI")
        with col4:
            render_status_badge(DEEPSEEK_AVAILABLE, "DeepSeek R1")



    # Alert for missing dependencies
    if not MEDIAPIPE_AVAILABLE:
        st.warning(
            "MediaPipe pose detection may have initialization issues. Voice Trainer will use basic mode."
        )
    else:
        st.success("✅ MediaPipe pose detection ready for advanced exercise tracking!")
    
    if not DEEPSEEK_AVAILABLE:
        st.warning(
            "🧠 DeepSeek R1 reasoning is disabled. Set DEEPSEEK_API_KEY environment variable to enable advanced fitness reasoning. See DEEPSEEK_SETUP.md for setup instructions."
        )
    
    if not ADVANCED_PLANNER_AVAILABLE:
        st.info(
            "📋 Advanced workout planner using basic mode. Install reportlab for PDF export: pip install reportlab"
        )
    
    if not NUTRITION_AI_AVAILABLE:
        st.info(
            "🍎 Nutrition AI Assistant disabled. Install PIL and OpenCV for meal photo analysis: pip install pillow opencv-python"
        )
    
    st.divider()

    # Main navigation tabs
    if AUTH_AVAILABLE and st.session_state.authenticated:
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
            [
                "Voice Trainer",
                "Diet Planner",
                "🍎 Nutrition AI",
                "Mental Health",
                "Workout Planner",
                "AI Assistant",
                "🏥 Health Data",
            ]
        )
    else:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
            [
                "Voice Trainer",
                "Diet Planner",
                "🍎 Nutrition AI",
                "Mental Health",
                "Workout Planner",
                "AI Assistant",
            ]
        )

    with tab1:
        with card_container():
            voice_trainer_ui()

    with tab2:
        with card_container():
            diet_planner_main()

    with tab3:
        with card_container():
            if NUTRITION_AI_AVAILABLE:
                nutrition_ai_assistant_ui()
            else:
                st.header("🍎 Nutrition AI Assistant")
                st.caption("Advanced nutrition analysis and meal planning")
                st.error("Nutrition AI Assistant not available - missing dependencies")
                st.info("Install PIL and cv2 for full Nutrition AI features: pip install pillow opencv-python")

    with tab4:
        with card_container():
            st.header("Mental Health Support")
            st.caption("Professional mental wellness guidance")
            mental_health_ui()

    with tab5:
        with card_container():
            smart_workout_ui()

    with tab6:
        with card_container():
            st.header("AI Assistant")
            st.caption("Intelligent fitness guidance and support")
            chat_ui()
    
    if AUTH_AVAILABLE and st.session_state.authenticated:
        with tab7:
            with card_container():
                st.header("🏥 Health Data Integration")
                st.caption("Sync and analyze your fitness data from wearables")
                
                if HEALTH_INTEGRATION_AVAILABLE:
                    # Initialize specialized health manager
                    health_manager = HealthDataManager()
                    user_id = st.session_state.user['user_id']
                    
                    health_tab1, health_tab2, health_tab3 = st.tabs(["📊 Data Input", "🏆 Analytics", "🔗 Google Fit"])
                
                    with health_tab1:
                        health_data_input_ui(user_id, health_manager)
                    
                    with health_tab2:
                        legendary_health_analytics(user_id, health_manager)
                    
                    with health_tab3:
                        google_fit_integration_ui(user_id)
                else:
                    st.error("Health integration modules not available. Please check dependencies.")


    # Sidebar navigation
    st.sidebar.title("Exercise Options")

    if MEDIAPIPE_AVAILABLE and EXERCISE_AVAILABLE:
        options = st.sidebar.selectbox(
            "Select Mode:",
            (
                "🎤 Voice Trainer",
                "📹 Video Analysis",
                "📷 WebCam Exercise",
                "🤖 Auto Classify",
            ),
        )
    else:
        st.sidebar.info("MediaPipe required for exercise features")
        options = "🎤 Voice Trainer"

    if options == "📹 Video Analysis" and MEDIAPIPE_AVAILABLE and EXERCISE_AVAILABLE:
        st.markdown("---")
        st.write("## 📹 Upload Video for Exercise Analysis")
        st.write("Upload your exercise video and get detailed form analysis")

        st.sidebar.markdown("---")
        exercise_options = st.sidebar.selectbox(
            "Select Exercise", ("Bicept Curl", "Push Up", "Squat", "Shoulder Press")
        )
        st.sidebar.markdown("---")
        video_file_buffer = st.sidebar.file_uploader(
            "Upload a video", type=["mp4", "mov", "avi", "asf", "m4v"]
        )

        if video_file_buffer:
            tfflie = tempfile.NamedTemporaryFile(delete=False)
            tfflie.write(video_file_buffer.read())
            cap = cv2.VideoCapture(tfflie.name)
            st.markdown("---")
            st.sidebar.text("Input Video")
            st.sidebar.video(tfflie.name)
            st.markdown("## Input Video")
            st.video(tfflie.name)
            st.markdown("---")

            st.markdown("## Output Video Analysis")
            if exercise_options == "Bicept Curl":
                exer = exercise.Exercise()
                counter, stage_right, stage_left = 0, None, None
                exer.bicept_curl(
                    cap,
                    is_video=True,
                    counter=counter,
                    stage_right=stage_right,
                    stage_left=stage_left,
                )

            elif exercise_options == "Push Up":
                st.write(
                    "The exercise needs to be filmed showing your left side or facing frontally"
                )
                exer = exercise.Exercise()
                counter, stage = 0, None
                exer.push_up(cap, is_video=True, counter=counter, stage=stage)

            elif exercise_options == "Squat":
                exer = exercise.Exercise()
                counter, stage = 0, None
                exer.squat(cap, is_video=True, counter=counter, stage=stage)

            elif exercise_options == "Shoulder Press":
                exer = exercise.Exercise()
                counter, stage = 0, None
                exer.shoulder_press(cap, is_video=True, counter=counter, stage=stage)

    elif options == "🤖 Auto Classify" and MEDIAPIPE_AVAILABLE and EXERCISE_AVAILABLE:
        st.markdown("---")
        st.write("## 🤖 Automatic Exercise Classification and Counting")
        st.write("AI will automatically detect and classify your exercise type")
        st.markdown("---")
        st.write(
            "Please ensure you are clearly visible and facing the camera directly. This will help the AI accurately track your movements."
        )

        auto_classify_button = st.button("Start Auto Classification")

        if auto_classify_button:
            time.sleep(2)
            try:
                exer = exercise.Exercise()
                exer.auto_classify_and_count()
            except Exception as e:
                st.error(f"Error accessing webcam: {str(e)}")
                st.info("Please make sure your webcam is connected and accessible.")

    elif options == "📷 WebCam Exercise" and MEDIAPIPE_AVAILABLE and EXERCISE_AVAILABLE:
        st.markdown("---")
        st.write("## 📷 WebCam Exercise Tracking")
        st.sidebar.markdown("---")

        exercise_general = st.sidebar.selectbox(
            "Select Exercise", ("Bicept Curl", "Push Up", "Squat", "Shoulder Press")
        )

        st.markdown("## WebCam Feed")
        st.write(
            "Please ensure you are clearly visible and facing the camera directly. This will help the AI accurately track your movements."
        )
        st.markdown("---")
        st.write(
            "Click button to start training. Say 'Hey Max' during exercise for assistance."
        )
        start_button = st.button("Start Exercise")

        if start_button:
            if exercise_coach:
                exercise_coach.start_exercise(
                    exercise_general.lower().replace(" ", "_")
                )
            time.sleep(2)
            try:
                ready = True
                if exercise_general == "Bicept Curl":
                    while ready:
                        cap = cv2.VideoCapture(0)
                        exer = exercise.Exercise()
                        counter, stage_right, stage_left = 0, None, None
                        exer.bicept_curl(
                            cap,
                            counter=counter,
                            stage_right=stage_right,
                            stage_left=stage_left,
                        )
                        break

                elif exercise_general == "Push Up":
                    st.write(
                        "The exercise needs to be filmed showing your left side or facing frontally"
                    )
                    while ready:
                        cap = cv2.VideoCapture(0)
                        exer = exercise.Exercise()
                        counter, stage = 0, None
                        exer.push_up(cap, counter=counter, stage=stage)
                        break

                elif exercise_general == "Squat":
                    while ready:
                        cap = cv2.VideoCapture(0)
                        exer = exercise.Exercise()
                        counter, stage = 0, None
                        exer.squat(cap, counter=counter, stage=stage)
                        break

                elif exercise_general == "Shoulder Press":
                    while ready:
                        cap = cv2.VideoCapture(0)
                        exer = exercise.Exercise()
                        counter, stage = 0, None
                        exer.shoulder_press(cap, counter=counter, stage=stage)
                        break
            except Exception as e:
                st.error(f"Error accessing webcam: {str(e)}")
                st.info("Please make sure your webcam is connected and accessible.")

    # Sidebar system information
    st.sidebar.divider()
    st.sidebar.subheader("System Information")
    
    if MEDIAPIPE_AVAILABLE:
        st.sidebar.success("Pose Detection: Ready")
    if ELEVENLABS_AVAILABLE:
        st.sidebar.success("Voice Feedback: Ready")
    if EXERCISE_AVAILABLE:
        st.sidebar.success("Exercise AI: Ready")
    if ADVANCED_PLANNER_AVAILABLE:
        st.sidebar.success("Smart Planner: Ready")
    if NUTRITION_AI_AVAILABLE:
        st.sidebar.success("Nutrition AI: Ready")

    st.sidebar.divider()
    st.sidebar.info(
        "**Recommendation**: Use Voice Trainer for form correction, Smart Planner for workouts, and Nutrition AI for comprehensive meal planning"
    )


if __name__ == "__main__":
    main()
