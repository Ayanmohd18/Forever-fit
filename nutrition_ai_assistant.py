#!/usr/bin/env python3

import streamlit as st
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO
import time

# Try to import image processing libraries
try:
    from PIL import Image
    import cv2
    import numpy as np
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False

# Try to import OpenAI for image analysis
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class NutritionDatabase:
    """Comprehensive nutrition database with food information"""
    
    def __init__(self):
        self.food_database = {
            # Proteins
            "chicken_breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6, "fiber": 0, "category": "protein"},
            "salmon": {"calories": 208, "protein": 22, "carbs": 0, "fat": 12, "fiber": 0, "category": "protein"},
            "eggs": {"calories": 155, "protein": 13, "carbs": 1.1, "fat": 11, "fiber": 0, "category": "protein"},
            "greek_yogurt": {"calories": 100, "protein": 17, "carbs": 6, "fat": 0.4, "fiber": 0, "category": "protein"},
            "tofu": {"calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "fiber": 0.3, "category": "protein"},
            
            # Carbohydrates
            "brown_rice": {"calories": 112, "protein": 2.6, "carbs": 23, "fat": 0.9, "fiber": 1.8, "category": "carbs"},
            "quinoa": {"calories": 120, "protein": 4.4, "carbs": 22, "fat": 1.9, "fiber": 2.8, "category": "carbs"},
            "sweet_potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1, "fiber": 3, "category": "carbs"},
            "oats": {"calories": 68, "protein": 2.4, "carbs": 12, "fat": 1.4, "fiber": 1.7, "category": "carbs"},
            "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3, "fiber": 2.6, "category": "carbs"},
            
            # Vegetables
            "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4, "fiber": 2.6, "category": "vegetables"},
            "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4, "fiber": 2.2, "category": "vegetables"},
            "bell_pepper": {"calories": 31, "protein": 1, "carbs": 7, "fat": 0.3, "fiber": 2.5, "category": "vegetables"},
            "carrots": {"calories": 41, "protein": 0.9, "carbs": 10, "fat": 0.2, "fiber": 2.8, "category": "vegetables"},
            "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fat": 0.2, "fiber": 1.2, "category": "vegetables"},
            
            # Fats
            "avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15, "fiber": 7, "category": "fats"},
            "almonds": {"calories": 164, "protein": 6, "carbs": 6, "fat": 14, "fiber": 3.5, "category": "fats"},
            "olive_oil": {"calories": 884, "protein": 0, "carbs": 0, "fat": 100, "fiber": 0, "category": "fats"},
            "walnuts": {"calories": 185, "protein": 4.3, "carbs": 3.9, "fat": 18.5, "fiber": 1.9, "category": "fats"},
        }
        
        self.restaurant_database = {
            "McDonald's": {
                "Big Mac": {"calories": 550, "protein": 25, "carbs": 45, "fat": 33, "fiber": 3},
                "Chicken McNuggets (6pc)": {"calories": 250, "protein": 15, "carbs": 15, "fat": 15, "fiber": 1},
                "Side Salad": {"calories": 15, "protein": 1, "carbs": 3, "fat": 0, "fiber": 2},
            },
            "Subway": {
                "Turkey Breast (6-inch)": {"calories": 280, "protein": 18, "carbs": 46, "fat": 3.5, "fiber": 5},
                "Chicken Teriyaki (6-inch)": {"calories": 370, "protein": 25, "carbs": 59, "fat": 4.5, "fiber": 5},
                "Veggie Delite (6-inch)": {"calories": 230, "protein": 8, "carbs": 44, "fat": 2.5, "fiber": 5},
            },
            "Chipotle": {
                "Chicken Bowl": {"calories": 540, "protein": 34, "carbs": 40, "fat": 21, "fiber": 12},
                "Burrito Bowl": {"calories": 665, "protein": 32, "carbs": 67, "fat": 25, "fiber": 13},
                "Salad Bowl": {"calories": 465, "protein": 32, "carbs": 20, "fat": 23, "fiber": 12},
            }
        }

class MealPhotoAnalyzer:
    """AI-powered meal photo analysis for macro counting"""
    
    def __init__(self):
        self.nutrition_db = NutritionDatabase()
    
    def analyze_meal_photo(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze uploaded meal photo and estimate nutritional content"""
        
        if not IMAGE_PROCESSING_AVAILABLE:
            return self._mock_analysis()
        
        # Convert PIL image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Basic image analysis (mock implementation)
        # In a real implementation, this would use computer vision models
        detected_foods = self._detect_foods_in_image(opencv_image)
        
        # Calculate total nutrition
        total_nutrition = self._calculate_total_nutrition(detected_foods)
        
        return {
            "detected_foods": detected_foods,
            "total_nutrition": total_nutrition,
            "confidence": 0.85,
            "analysis_time": datetime.now().isoformat()
        }
    
    def _detect_foods_in_image(self, image) -> List[Dict]:
        """Mock food detection - in reality would use trained ML models"""
        # This is a simplified mock - real implementation would use:
        # - YOLO or similar object detection models
        # - Food-specific trained models
        # - Portion size estimation algorithms
        
        mock_foods = [
            {"name": "chicken_breast", "portion_size": 150, "confidence": 0.9},
            {"name": "brown_rice", "portion_size": 100, "confidence": 0.8},
            {"name": "broccoli", "portion_size": 80, "confidence": 0.85}
        ]
        return mock_foods
    
    def _calculate_total_nutrition(self, detected_foods: List[Dict]) -> Dict:
        """Calculate total nutritional content from detected foods"""
        total = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
        
        for food in detected_foods:
            food_name = food["name"]
            portion_g = food["portion_size"]
            
            if food_name in self.nutrition_db.food_database:
                food_data = self.nutrition_db.food_database[food_name]
                # Nutrition data is per 100g, so scale by portion
                scale = portion_g / 100
                
                total["calories"] += food_data["calories"] * scale
                total["protein"] += food_data["protein"] * scale
                total["carbs"] += food_data["carbs"] * scale
                total["fat"] += food_data["fat"] * scale
                total["fiber"] += food_data["fiber"] * scale
        
        # Round values
        for key in total:
            total[key] = round(total[key], 1)
        
        return total
    
    def _mock_analysis(self) -> Dict[str, Any]:
        """Fallback mock analysis when image processing is unavailable"""
        return {
            "detected_foods": [
                {"name": "mixed_meal", "portion_size": 300, "confidence": 0.7}
            ],
            "total_nutrition": {
                "calories": 450,
                "protein": 25,
                "carbs": 35,
                "fat": 18,
                "fiber": 5
            },
            "confidence": 0.7,
            "analysis_time": datetime.now().isoformat(),
            "note": "Mock analysis - install PIL and cv2 for real image processing"
        }

class PersonalizedMealPlanner:
    """Generate personalized meal plans based on workout schedule and goals"""
    
    def __init__(self):
        self.nutrition_db = NutritionDatabase()
    
    def generate_meal_plan(self, user_profile: Dict, workout_schedule: Dict) -> Dict:
        """Generate a personalized weekly meal plan"""
        
        # Calculate daily caloric needs
        daily_calories = self._calculate_daily_calories(user_profile)
        
        # Adjust for workout days
        meal_plan = {}
        
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            is_workout_day = day in workout_schedule.get("workout_days", [])
            
            if is_workout_day:
                day_calories = daily_calories + 200  # Extra calories for workout days
            else:
                day_calories = daily_calories
            
            meal_plan[day] = self._generate_daily_meals(day_calories, user_profile, is_workout_day)
        
        return {
            "weekly_plan": meal_plan,
            "daily_targets": {
                "calories": daily_calories,
                "protein": user_profile.get("weight", 70) * 1.6,  # 1.6g per kg
                "carbs": daily_calories * 0.45 / 4,  # 45% of calories
                "fat": daily_calories * 0.25 / 9,  # 25% of calories
            },
            "generated_date": datetime.now().isoformat()
        }
    
    def _calculate_daily_calories(self, user_profile: Dict) -> int:
        """Calculate daily caloric needs using Mifflin-St Jeor equation"""
        
        weight = user_profile.get("weight", 70)
        height = user_profile.get("height", 170)
        age = user_profile.get("age", 30)
        gender = user_profile.get("gender", "male").lower()
        activity_level = user_profile.get("activity_level", "moderate")
        goal = user_profile.get("goal", "maintain").lower()
        
        # Base Metabolic Rate
        if gender == "male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multipliers
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # Adjust for goals
        if "lose" in goal or "cut" in goal:
            return int(tdee - 500)  # 500 calorie deficit
        elif "gain" in goal or "bulk" in goal:
            return int(tdee + 300)  # 300 calorie surplus
        else:
            return int(tdee)  # Maintenance
    
    def _generate_daily_meals(self, target_calories: int, user_profile: Dict, is_workout_day: bool) -> Dict:
        """Generate meals for a single day"""
        
        # Meal distribution
        breakfast_cals = int(target_calories * 0.25)
        lunch_cals = int(target_calories * 0.35)
        dinner_cals = int(target_calories * 0.30)
        snack_cals = int(target_calories * 0.10)
        
        if is_workout_day:
            # Add pre/post workout snacks
            pre_workout = {"name": "Pre-workout", "foods": ["banana", "oats"], "calories": 150}
            post_workout = {"name": "Post-workout", "foods": ["greek_yogurt", "almonds"], "calories": 200}
        else:
            pre_workout = None
            post_workout = None
        
        return {
            "breakfast": self._create_meal("Breakfast", breakfast_cals, ["protein", "carbs"]),
            "lunch": self._create_meal("Lunch", lunch_cals, ["protein", "carbs", "vegetables"]),
            "dinner": self._create_meal("Dinner", dinner_cals, ["protein", "vegetables", "fats"]),
            "snacks": self._create_meal("Snacks", snack_cals, ["fats", "protein"]),
            "pre_workout": pre_workout,
            "post_workout": post_workout,
            "total_calories": target_calories,
            "is_workout_day": is_workout_day
        }
    
    def _create_meal(self, meal_name: str, target_calories: int, preferred_categories: List[str]) -> Dict:
        """Create a balanced meal within calorie target"""
        
        selected_foods = []
        current_calories = 0
        
        # Select foods from preferred categories
        for category in preferred_categories:
            category_foods = [
                (name, data) for name, data in self.nutrition_db.food_database.items()
                if data["category"] == category
            ]
            
            if category_foods:
                food_name, food_data = category_foods[0]  # Simple selection
                portion = min(150, (target_calories - current_calories) / food_data["calories"] * 100)
                
                if portion > 20:  # Minimum 20g portion
                    selected_foods.append({
                        "name": food_name.replace("_", " ").title(),
                        "portion_g": round(portion),
                        "calories": round(food_data["calories"] * portion / 100)
                    })
                    current_calories += food_data["calories"] * portion / 100
        
        return {
            "name": meal_name,
            "foods": selected_foods,
            "total_calories": round(current_calories),
            "target_calories": target_calories
        }

class GroceryListGenerator:
    """Generate grocery lists from meal plans"""
    
    def __init__(self):
        self.nutrition_db = NutritionDatabase()
    
    def generate_grocery_list(self, meal_plan: Dict, servings: int = 1) -> Dict:
        """Generate a grocery list from a meal plan"""
        
        grocery_items = {}
        
        # Extract all foods from meal plan
        for day, meals in meal_plan["weekly_plan"].items():
            for meal_name, meal_data in meals.items():
                if meal_data and isinstance(meal_data, dict) and "foods" in meal_data:
                    for food in meal_data["foods"]:
                        if isinstance(food, dict) and "name" in food:
                            food_name = food["name"]
                            portion = food.get("portion_g", 100)
                            
                            if food_name in grocery_items:
                                grocery_items[food_name] += portion * servings
                            else:
                                grocery_items[food_name] = portion * servings
        
        # Organize by categories
        categorized_list = {
            "Proteins": [],
            "Carbohydrates": [],
            "Vegetables": [],
            "Fats & Oils": [],
            "Other": []
        }
        
        category_mapping = {
            "protein": "Proteins",
            "carbs": "Carbohydrates", 
            "vegetables": "Vegetables",
            "fats": "Fats & Oils"
        }
        
        for food_name, total_amount in grocery_items.items():
            # Find category
            food_key = food_name.lower().replace(" ", "_")
            category = "Other"
            
            if food_key in self.nutrition_db.food_database:
                food_category = self.nutrition_db.food_database[food_key]["category"]
                category = category_mapping.get(food_category, "Other")
            
            categorized_list[category].append({
                "name": food_name,
                "amount": f"{round(total_amount)}g",
                "estimated_cost": self._estimate_cost(food_name, total_amount)
            })
        
        return {
            "grocery_list": categorized_list,
            "total_estimated_cost": sum(
                item["estimated_cost"] 
                for category in categorized_list.values() 
                for item in category
            ),
            "generated_date": datetime.now().isoformat(),
            "servings": servings
        }
    
    def _estimate_cost(self, food_name: str, amount_g: float) -> float:
        """Estimate cost of food item (mock implementation)"""
        # Mock pricing per 100g
        price_per_100g = {
            "chicken_breast": 3.50,
            "salmon": 8.00,
            "eggs": 2.00,
            "greek_yogurt": 1.50,
            "brown_rice": 0.80,
            "quinoa": 2.50,
            "sweet_potato": 1.20,
            "broccoli": 2.00,
            "spinach": 2.50,
            "avocado": 4.00,
            "almonds": 6.00
        }
        
        food_key = food_name.lower().replace(" ", "_")
        price = price_per_100g.get(food_key, 2.00)  # Default $2 per 100g
        
        return round((amount_g / 100) * price, 2)

class RestaurantRecommendationEngine:
    """Provide healthy restaurant meal recommendations"""
    
    def __init__(self):
        self.nutrition_db = NutritionDatabase()
    
    def get_restaurant_recommendations(self, user_goals: Dict, location: str = "nearby") -> Dict:
        """Get restaurant recommendations based on user goals"""
        
        goal = user_goals.get("primary_goal", "maintain").lower()
        daily_calories = user_goals.get("daily_calories", 2000)
        meal_calories = daily_calories // 3  # Assume this is for one meal
        
        recommendations = []
        
        for restaurant, menu in self.nutrition_db.restaurant_database.items():
            for item_name, nutrition in menu.items():
                # Filter based on goals
                if self._matches_goals(nutrition, goal, meal_calories):
                    recommendations.append({
                        "restaurant": restaurant,
                        "item": item_name,
                        "nutrition": nutrition,
                        "fit_score": self._calculate_fit_score(nutrition, goal, meal_calories),
                        "modifications": self._suggest_modifications(nutrition, goal)
                    })
        
        # Sort by fit score
        recommendations.sort(key=lambda x: x["fit_score"], reverse=True)
        
        return {
            "recommendations": recommendations[:10],  # Top 10
            "location": location,
            "generated_date": datetime.now().isoformat(),
            "user_goals": user_goals
        }
    
    def _matches_goals(self, nutrition: Dict, goal: str, target_calories: int) -> bool:
        """Check if menu item matches user goals"""
        calories = nutrition["calories"]
        protein = nutrition["protein"]
        
        # Basic filtering
        if calories > target_calories * 1.5:  # Too high in calories
            return False
        
        if "lose" in goal and calories > target_calories:
            return False
        
        if protein < 15 and "muscle" in goal:  # Need adequate protein
            return False
        
        return True
    
    def _calculate_fit_score(self, nutrition: Dict, goal: str, target_calories: int) -> float:
        """Calculate how well the item fits user goals (0-100)"""
        score = 50  # Base score
        
        calories = nutrition["calories"]
        protein = nutrition["protein"]
        fat = nutrition["fat"]
        
        # Calorie alignment
        calorie_diff = abs(calories - target_calories) / target_calories
        score += (1 - calorie_diff) * 30
        
        # Protein content
        if protein >= 20:
            score += 15
        elif protein >= 15:
            score += 10
        
        # Fat content (moderate is good)
        if 10 <= fat <= 25:
            score += 10
        
        # Goal-specific adjustments
        if "lose" in goal and calories < target_calories * 0.8:
            score += 10
        
        if "muscle" in goal and protein >= 25:
            score += 15
        
        return min(100, max(0, score))
    
    def _suggest_modifications(self, nutrition: Dict, goal: str) -> List[str]:
        """Suggest modifications to make the meal better for goals"""
        modifications = []
        
        if nutrition["calories"] > 600:
            modifications.append("Ask for half portion or share")
        
        if nutrition["fat"] > 30:
            modifications.append("Request dressing/sauce on the side")
        
        if "lose" in goal:
            modifications.append("Substitute fries with salad")
            modifications.append("Choose grilled over fried")
        
        if "muscle" in goal and nutrition["protein"] < 25:
            modifications.append("Add extra protein")
        
        return modifications

def nutrition_ai_assistant_ui():
    """Main UI for the Nutrition AI Assistant"""
    
    st.title("🍎 Nutrition AI Assistant")
    st.markdown("*Complete nutrition analysis, meal planning, and smart recommendations*")
    
    # Initialize components
    photo_analyzer = MealPhotoAnalyzer()
    meal_planner = PersonalizedMealPlanner()
    grocery_generator = GroceryListGenerator()
    restaurant_engine = RestaurantRecommendationEngine()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📸 Photo Analysis", 
        "🍽️ Meal Planner", 
        "🛒 Grocery Lists", 
        "🏪 Restaurant Guide",
        "📊 Nutrition Tracker"
    ])
    
    with tab1:
        st.header("📸 Meal Photo Analysis")
        st.caption("Upload a photo of your meal for instant macro counting")
        
        # Photo upload
        uploaded_file = st.file_uploader(
            "Choose a meal photo", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of your meal for AI analysis"
        )
        
        if uploaded_file is not None:
            # Display image
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.image(image, caption="Uploaded Meal", use_container_width=True)
            
            with col2:
                if st.button("🔍 Analyze Meal", type="primary"):
                    with st.spinner("🧠 AI analyzing your meal..."):
                        analysis = photo_analyzer.analyze_meal_photo(image)
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Display results
                    nutrition = analysis["total_nutrition"]
                    
                    # Nutrition metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Calories", f"{nutrition['calories']}")
                    with col2:
                        st.metric("Protein", f"{nutrition['protein']}g")
                    with col3:
                        st.metric("Carbs", f"{nutrition['carbs']}g")
                    with col4:
                        st.metric("Fat", f"{nutrition['fat']}g")
                    
                    # Detected foods
                    st.subheader("🔍 Detected Foods")
                    for food in analysis["detected_foods"]:
                        st.write(f"• **{food['name'].replace('_', ' ').title()}** - {food['portion_size']}g (Confidence: {food['confidence']:.0%})")
                    
                    # Save option
                    if st.button("💾 Save to Food Log"):
                        if "food_log" not in st.session_state:
                            st.session_state.food_log = []
                        
                        st.session_state.food_log.append({
                            "date": datetime.now().isoformat(),
                            "meal_type": st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"]),
                            "nutrition": nutrition,
                            "foods": analysis["detected_foods"]
                        })
                        st.success("Meal saved to your food log!")
        
        # Manual entry option
        st.divider()
        st.subheader("✏️ Manual Entry")
        st.caption("Can't upload a photo? Enter your meal manually")
        
        with st.expander("Add Food Manually"):
            food_name = st.text_input("Food Name")
            portion_size = st.number_input("Portion Size (g)", min_value=1, value=100)
            
            if st.button("Add Food"):
                st.info("Manual food entry feature - would integrate with nutrition database")
    
    with tab2:
        st.header("🍽️ Personalized Meal Planner")
        st.caption("AI-generated meal plans based on your workout schedule and goals")
        
        # User profile input
        with st.expander("👤 Your Profile", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                age = st.number_input("Age", min_value=16, max_value=80, value=30)
                weight = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
                height = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
            
            with col2:
                gender = st.selectbox("Gender", ["Male", "Female"])
                activity_level = st.selectbox("Activity Level", [
                    "Sedentary", "Light", "Moderate", "Active", "Very Active"
                ])
                goal = st.selectbox("Primary Goal", [
                    "Lose Weight", "Maintain Weight", "Gain Muscle", "Improve Performance"
                ])
        
        # Workout schedule
        st.subheader("🏋️ Workout Schedule")
        workout_days = st.multiselect(
            "Select your workout days:",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            default=["Monday", "Wednesday", "Friday"]
        )
        
        # Generate meal plan
        if st.button("🎯 Generate Personalized Meal Plan", type="primary"):
            user_profile = {
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender.lower(),
                "activity_level": activity_level.lower(),
                "goal": goal.lower()
            }
            
            workout_schedule = {"workout_days": workout_days}
            
            with st.spinner("🧠 Creating your personalized meal plan..."):
                meal_plan = meal_planner.generate_meal_plan(user_profile, workout_schedule)
            
            st.success("✅ Your meal plan is ready!")
            
            # Display daily targets
            targets = meal_plan["daily_targets"]
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Daily Calories", f"{targets['calories']}")
            with col2:
                st.metric("Protein Target", f"{targets['protein']:.0f}g")
            with col3:
                st.metric("Carbs Target", f"{targets['carbs']:.0f}g")
            with col4:
                st.metric("Fat Target", f"{targets['fat']:.0f}g")
            
            # Weekly meal plan
            st.subheader("📅 Your Weekly Meal Plan")
            
            for day, meals in meal_plan["weekly_plan"].items():
                with st.expander(f"{day} {'🏋️' if day in workout_days else '🛋️'}"):
                    for meal_name, meal_data in meals.items():
                        if meal_data and isinstance(meal_data, dict):
                            st.write(f"**{meal_data.get('name', meal_name)}** ({meal_data.get('total_calories', 0)} cal)")
                            if "foods" in meal_data:
                                for food in meal_data["foods"]:
                                    if isinstance(food, dict):
                                        st.write(f"  • {food.get('name', 'Unknown')} - {food.get('portion_g', 0)}g")
            
            # Save meal plan
            if st.button("💾 Save Meal Plan"):
                st.session_state.current_meal_plan = meal_plan
                st.success("Meal plan saved!")
    
    with tab3:
        st.header("🛒 Smart Grocery Lists")
        st.caption("Automatically generated grocery lists from your meal plans")
        
        if "current_meal_plan" in st.session_state:
            meal_plan = st.session_state.current_meal_plan
            
            # Servings input
            servings = st.number_input("Number of servings/people", min_value=1, max_value=10, value=1)
            
            if st.button("📝 Generate Grocery List", type="primary"):
                with st.spinner("📋 Creating your grocery list..."):
                    grocery_list = grocery_generator.generate_grocery_list(meal_plan, servings)
                
                st.success("✅ Grocery list ready!")
                
                # Display total cost
                st.metric("Estimated Total Cost", f"${grocery_list['total_estimated_cost']:.2f}")
                
                # Display categorized list
                for category, items in grocery_list["grocery_list"].items():
                    if items:  # Only show categories with items
                        st.subheader(f"🏷️ {category}")
                        for item in items:
                            col1, col2, col3 = st.columns([3, 1, 1])
                            with col1:
                                st.write(f"• {item['name']}")
                            with col2:
                                st.write(item['amount'])
                            with col3:
                                st.write(f"${item['estimated_cost']:.2f}")
                
                # Download options
                st.divider()
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📱 Export to Phone"):
                        st.info("Feature: Export grocery list to mobile app")
                
                with col2:
                    grocery_text = "\n".join([
                        f"{category}:\n" + "\n".join([f"  • {item['name']} - {item['amount']}" for item in items])
                        for category, items in grocery_list["grocery_list"].items() if items
                    ])
                    
                    st.download_button(
                        "📄 Download List",
                        grocery_text,
                        file_name=f"grocery_list_{datetime.now().strftime('%Y%m%d')}.txt",
                        mime="text/plain"
                    )
        else:
            st.info("👆 Generate a meal plan first to create grocery lists")
    
    with tab4:
        st.header("🏪 Restaurant Recommendation Engine")
        st.caption("Find healthy options when eating out")
        
        # User goals input
        col1, col2 = st.columns(2)
        
        with col1:
            primary_goal = st.selectbox("Primary Goal", [
                "Lose Weight", "Maintain Weight", "Build Muscle", "General Health"
            ])
            daily_calories = st.number_input("Daily Calorie Target", min_value=1200, max_value=4000, value=2000)
        
        with col2:
            location = st.text_input("Location", value="Nearby")
            meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack"])
        
        if st.button("🔍 Find Healthy Options", type="primary"):
            user_goals = {
                "primary_goal": primary_goal.lower(),
                "daily_calories": daily_calories,
                "meal_type": meal_type.lower()
            }
            
            with st.spinner("🔍 Finding the best options for you..."):
                recommendations = restaurant_engine.get_restaurant_recommendations(user_goals, location)
            
            st.success(f"✅ Found {len(recommendations['recommendations'])} great options!")
            
            # Display recommendations
            for i, rec in enumerate(recommendations["recommendations"], 1):
                with st.expander(f"{i}. {rec['restaurant']} - {rec['item']} (Fit Score: {rec['fit_score']:.0f}/100)"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        nutrition = rec["nutrition"]
                        st.write(f"**Calories:** {nutrition['calories']} | **Protein:** {nutrition['protein']}g | **Carbs:** {nutrition['carbs']}g | **Fat:** {nutrition['fat']}g")
                        
                        if rec["modifications"]:
                            st.write("**💡 Suggested Modifications:**")
                            for mod in rec["modifications"]:
                                st.write(f"  • {mod}")
                    
                    with col2:
                        if st.button(f"📍 Get Directions", key=f"directions_{i}"):
                            st.info(f"Opening directions to {rec['restaurant']}")
        
        # Quick filters
        st.divider()
        st.subheader("🎯 Quick Filters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🥗 Low Calorie Options"):
                st.info("Filtering for meals under 400 calories")
        
        with col2:
            if st.button("💪 High Protein Options"):
                st.info("Filtering for meals with 25+ grams protein")
        
        with col3:
            if st.button("🌱 Vegetarian Options"):
                st.info("Filtering for vegetarian-friendly meals")
    
    with tab5:
        st.header("📊 Nutrition Tracker")
        st.caption("Track your daily nutrition and progress")
        
        # Daily summary
        if "food_log" in st.session_state and st.session_state.food_log:
            today_log = [
                entry for entry in st.session_state.food_log 
                if datetime.fromisoformat(entry["date"]).date() == datetime.now().date()
            ]
            
            if today_log:
                # Calculate daily totals
                daily_totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
                
                for entry in today_log:
                    nutrition = entry["nutrition"]
                    for key in daily_totals:
                        daily_totals[key] += nutrition.get(key, 0)
                
                st.subheader("📈 Today's Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Calories", f"{daily_totals['calories']:.0f}")
                with col2:
                    st.metric("Protein", f"{daily_totals['protein']:.1f}g")
                with col3:
                    st.metric("Carbs", f"{daily_totals['carbs']:.1f}g")
                with col4:
                    st.metric("Fat", f"{daily_totals['fat']:.1f}g")
                
                # Progress bars (assuming 2000 cal, 150g protein targets)
                st.subheader("🎯 Daily Progress")
                
                cal_progress = min(100, (daily_totals['calories'] / 2000) * 100)
                protein_progress = min(100, (daily_totals['protein'] / 150) * 100)
                
                st.progress(cal_progress / 100, text=f"Calories: {cal_progress:.0f}%")
                st.progress(protein_progress / 100, text=f"Protein: {protein_progress:.0f}%")
                
                # Recent meals
                st.subheader("🍽️ Recent Meals")
                for entry in reversed(today_log[-5:]):  # Last 5 meals
                    meal_time = datetime.fromisoformat(entry["date"]).strftime("%H:%M")
                    st.write(f"**{meal_time}** - {entry.get('meal_type', 'Unknown')} ({entry['nutrition']['calories']:.0f} cal)")
            else:
                st.info("No meals logged today. Start by analyzing a meal photo!")
        else:
            st.info("No nutrition data yet. Use the Photo Analysis tab to start tracking!")
        
        # Weekly trends (mock)
        st.divider()
        st.subheader("📈 Weekly Trends")
        st.info("Weekly nutrition trends would be displayed here with charts")

if __name__ == "__main__":
    nutrition_ai_assistant_ui()