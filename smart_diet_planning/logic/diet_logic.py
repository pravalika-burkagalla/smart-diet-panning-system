def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m ** 2), 2)


def calculate_bmr(weight, height_cm, age, gender):
    if gender.lower() == "male":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height_cm - 5 * age - 161


def get_age_group_data(age):
    """
    Get age group information including typical BMI ranges and calorie recommendations.
    
    Args:
        age: Age in years
        
    Returns:
        Dictionary with age group info
    """
    if age < 2:
        return {
            "group": "Infant",
            "bmi_info": "BMI not typically used for infants",
            "calorie_info": "Consult pediatrician for specific needs"
        }
    elif 2 <= age <= 12:
        return {
            "group": "Children (2-12)",
            "bmi_info": "BMI percentiles: 5th-85th percentile is normal",
            "calorie_info": f"Children {age} years: {1000 + (age-2)*100} calories/day (approximate)"
        }
    elif 13 <= age <= 19:
        return {
            "group": "Teens (13-19)",
            "bmi_info": "BMI percentiles: 5th-85th percentile is normal",
            "calorie_info": f"Teens {age} years: Males ~2800, Females ~2200 calories/day"
        }
    elif 20 <= age <= 64:
        return {
            "group": "Adults (20-64)",
            "bmi_info": "Normal BMI: 18.5-24.9, Overweight: 25-29.9, Obese: ≥30",
            "calorie_info": "Adults: Males ~2500, Females ~2000 calories/day (varies by activity)"
        }
    else:  # 65+
        return {
            "group": "Seniors (65+)",
            "bmi_info": "Normal BMI: 22-27 (slightly higher than younger adults)",
            "calorie_info": f"Seniors {age} years: Males ~2200, Females ~1800 calories/day"
        }


def calorie_requirement(bmr, activity):
    factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    return round(bmr * factors.get(activity, 1.2))


def generate_diet_plan(food_items, calories, goal):
    """
    Generate a personalized diet plan based on calorie target and fitness goal.
    
    Args:
        food_items: List of food tuples from database
        calories: Daily calorie target
        goal: 'loss', 'gain', or 'maintain'
    
    Returns:
        Dictionary with meal recommendations for each meal time
    """
    plan = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snack": []}
    
    # Separate foods by meal type
    breakfast_foods = [item for item in food_items if item[5] == "Breakfast"]
    lunch_foods = [item for item in food_items if item[5] == "Lunch"]
    dinner_foods = [item for item in food_items if item[5] == "Dinner"]
    snack_foods = [item for item in food_items if item[5] == "Snack"]
    
    # Calorie distribution for meals
    breakfast_cal = calories * 0.25  # 25% for breakfast
    lunch_cal = calories * 0.35      # 35% for lunch
    dinner_cal = calories * 0.30     # 30% for dinner
    snack_cal = calories * 0.10      # 10% for snacks
    
    # For weight loss: prioritize low-calorie, high-protein foods
    if goal == "loss":
        plan["Breakfast"] = [item[0] for item in breakfast_foods if item[2] <= breakfast_cal + 100][:3]
        plan["Lunch"] = [item[0] for item in sorted(lunch_foods, key=lambda x: -x[2])[:8] if item[2] <= lunch_cal + 100][:3]
        plan["Dinner"] = [item[0] for item in sorted(dinner_foods, key=lambda x: -x[2])[:8] if item[2] <= dinner_cal + 100][:3]
        plan["Snack"] = [item[0] for item in snack_foods if item[2] <= snack_cal + 50][:2]
    
    # For weight gain: prioritize high-calorie, high-protein foods
    elif goal == "gain":
        plan["Breakfast"] = [item[0] for item in sorted(breakfast_foods, key=lambda x: -x[2])[:5]][:2]
        plan["Lunch"] = [item[0] for item in sorted(lunch_foods, key=lambda x: -x[2])[:8]][:3]
        plan["Dinner"] = [item[0] for item in sorted(dinner_foods, key=lambda x: -x[2])[:8]][:3]
        plan["Snack"] = [item[0] for item in sorted(snack_foods, key=lambda x: -x[2])[:6]][:2]
    
    # For maintenance: balanced approach
    else:  # maintain
        plan["Breakfast"] = [item[0] for item in breakfast_foods[1:4]][:2]
        plan["Lunch"] = [item[0] for item in lunch_foods[2:6]][:3]
        plan["Dinner"] = [item[0] for item in dinner_foods[2:6]][:3]
        plan["Snack"] = [item[0] for item in snack_foods[2:5]][:2]
    
    return plan


def generate_diet_plan_improved(food_items, calories, goal, bmi_category=None, age=None, gender=None):
    """
    Generate a personalized diet plan based on calorie target, fitness goal, and body details.
    This improved version considers BMI category, age, and gender for more personalized recommendations.

    Args:
        food_items: List of food tuples from database (name, calories, protein, carbs, fats, meal_type)
        calories: Daily calorie target
        goal: 'loss', 'gain', or 'maintain'
        bmi_category: BMI category ('underweight', 'normal', 'overweight', 'obese')
        age: Age in years
        gender: 'male' or 'female'

    Returns:
        Dictionary with meal recommendations for each meal time
    """
    plan = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snack": []}

    # Separate foods by meal type
    breakfast_foods = [item for item in food_items if item[5] == "Breakfast"]
    lunch_foods = [item for item in food_items if item[5] == "Lunch"]
    dinner_foods = [item for item in food_items if item[5] == "Dinner"]
    snack_foods = [item for item in food_items if item[5] == "Snack"]

    # Ensure we have foods for each meal type, use alternatives if needed
    if not breakfast_foods:
        breakfast_foods = food_items[:5]  # Fallback to any foods
    if not lunch_foods:
        lunch_foods = food_items[5:15] if len(food_items) > 15 else food_items
    if not dinner_foods:
        dinner_foods = food_items[15:25] if len(food_items) > 25 else food_items
    if not snack_foods:
        snack_foods = food_items[-5:] if len(food_items) > 5 else food_items

    def select_meals(food_list, num_meals, goal="maintain", bmi_category=None, age=None):
        """
        Select meals with fallback logic to ensure recommendations are always provided.
        Considers goal, BMI category, and age for personalized selections.
        """
        if not food_list:
            return []

        if len(food_list) <= num_meals:
            return [item[0] for item in food_list]

        # Goal-specific sorting
        if goal == "loss":
            # Low calorie with higher protein
            sorted_foods = sorted(food_list, key=lambda x: (x[1], -x[2]))
        elif goal == "gain":
            # High calorie with higher protein
            sorted_foods = sorted(food_list, key=lambda x: (-x[1], -x[2]))
        else:
            # Maintain: closest to median calories and good protein
            calories = [item[1] for item in food_list]
            median_cal = sorted(calories)[len(calories)//2]
            sorted_foods = sorted(food_list, key=lambda x: (abs(x[1]-median_cal), -x[2]))

        # BMI adjustments if needed
        if bmi_category == "underweight" and goal == "gain":
            sorted_foods = sorted(food_list, key=lambda x: (-x[1], -x[2]))
        elif bmi_category in ["overweight", "obese"] and goal == "loss":
            sorted_foods = sorted(food_list, key=lambda x: (x[1], -x[2]))

        # Child and senior preferences
        if age and age < 18:
            sorted_foods = sorted(sorted_foods, key=lambda x: -x[2])
        elif age and age >= 65:
            sorted_foods = sorted(sorted_foods, key=lambda x: (-x[2], x[1]))

        return [item[0] for item in sorted_foods[:num_meals]]

    # Generate meal plans based on goal, considering BMI category and age
    if goal == "loss":
        # Weight loss: focus on low-calorie, high-protein choices for each meal
        plan["Breakfast"] = select_meals(breakfast_foods, 3, "loss", bmi_category, age)
        plan["Lunch"] = select_meals(lunch_foods, 3, "loss", bmi_category, age)
        plan["Dinner"] = select_meals(dinner_foods, 3, "loss", bmi_category, age)
        plan["Snack"] = select_meals(snack_foods, 2, "loss", bmi_category, age)

    elif goal == "gain":
        # Weight gain: focus on higher calorie nutrient-dense choices for each meal
        plan["Breakfast"] = select_meals(breakfast_foods, 3, "gain", bmi_category, age)
        plan["Lunch"] = select_meals(lunch_foods, 3, "gain", bmi_category, age)
        plan["Dinner"] = select_meals(dinner_foods, 3, "gain", bmi_category, age)
        plan["Snack"] = select_meals(snack_foods, 2, "gain", bmi_category, age)

    else:  # maintain
        # Maintenance: Balanced approach with moderate calories
        plan["Breakfast"] = select_meals(breakfast_foods, 3, "maintain", bmi_category, age)
        plan["Lunch"] = select_meals(lunch_foods, 3, "maintain", bmi_category, age)
        plan["Dinner"] = select_meals(dinner_foods, 3, "maintain", bmi_category, age)
        plan["Snack"] = select_meals(snack_foods, 2, "maintain", bmi_category, age)

    # Age and gender specific adjustments
    if age and age < 18:
        # For children/teens: adjust portions and focus on growth nutrients
        # Reduce number of items slightly for younger ages
        for meal_type in plan:
            if len(plan[meal_type]) > 2:
                plan[meal_type] = plan[meal_type][:2]
    
    elif age and age > 65:
        # For seniors: focus on nutrient density and easier digestion
        # Ensure good protein sources for muscle maintenance
        pass  # The balanced selection already prioritizes protein

    # Gender-specific adjustments (minor)
    if gender and gender.lower() == "female":
        # Women might need slightly more calcium-rich foods
        pass  # Could be enhanced with calcium-focused food database
    
    if gender and gender.lower() == "male":
        # Men might need slightly more protein
        pass  # The protein sorting already helps

    # Final fallback: If any meal type is still empty, add some general recommendations
    all_foods = [item[0] for item in food_items]
    if not plan["Breakfast"] and all_foods:
        plan["Breakfast"] = all_foods[:3]
    if not plan["Lunch"] and all_foods:
        plan["Lunch"] = all_foods[3:6] if len(all_foods) > 6 else all_foods[:3]
    if not plan["Dinner"] and all_foods:
        plan["Dinner"] = all_foods[6:9] if len(all_foods) > 9 else all_foods[:3]
    if not plan["Snack"] and all_foods:
        plan["Snack"] = all_foods[-3:] if len(all_foods) > 3 else all_foods[:2]

    return plan 
def get_bmi_category(bmi, age):
    """
    Determine BMI category based on BMI value and age.
    
    Args:
        bmi: Body Mass Index value
        age: Age in years
        
    Returns:
        String representing BMI category
    """
    if age < 20:
        # For children and teens, BMI categories are based on percentiles
        # This is a simplified approach - in reality, percentiles are used
        if bmi < 18.5:
            return "underweight"
        elif 18.5 <= bmi < 25:
            return "normal"
        elif 25 <= bmi < 30:
            return "overweight"
        else:
            return "obese"
    else:
        # Adult BMI categories
        if bmi < 18.5:
            return "underweight"
        elif 18.5 <= bmi < 25:
            return "normal"
        elif 25 <= bmi < 30:
            return "overweight"
        else:
            return "obese"


def get_exercise_recommendations(bmi_category, age, activity_level):
    """
    Get exercise recommendations based on BMI category, age, and activity level.
    
    Args:
        bmi_category: BMI category (underweight, normal, overweight, obese)
        age: Age in years
        activity_level: Current activity level
        
    Returns:
        Dictionary with exercise recommendations
    """
    recommendations = {
        "underweight": {
            "focus": "Build muscle mass and strength",
            "exercises": [
                "Strength training 3-4 times per week",
                "Compound exercises: Squats, deadlifts, bench press",
                "Progressive overload - gradually increase weights",
                "Light cardio 2-3 times per week (20-30 minutes)",
                "Yoga or Pilates for flexibility and core strength"
            ],
            "duration": "45-60 minutes per session",
            "tips": [
                "Focus on building muscle rather than burning calories",
                "Rest adequately between workouts",
                "Combine with proper nutrition for best results"
            ]
        },
        "normal": {
            "focus": "Maintain fitness and health",
            "exercises": [
                "Mix of cardio and strength training",
                "30-45 minutes of moderate cardio 3-5 times/week",
                "Strength training 2-3 times per week",
                "Flexibility exercises like yoga or stretching",
                "Sports or recreational activities you enjoy"
            ],
            "duration": "30-45 minutes per session",
            "tips": [
                "Balance cardio and strength training",
                "Include variety to prevent boredom",
                "Listen to your body and rest when needed"
            ]
        },
        "overweight": {
            "focus": "Gradual weight loss and improved fitness",
            "exercises": [
                "Walking or brisk walking 30-60 minutes daily",
                "Low-impact cardio: Swimming, cycling, elliptical",
                "Strength training 2-3 times per week",
                "Bodyweight exercises: Push-ups, squats, lunges",
                "Gradually increase intensity as fitness improves"
            ],
            "duration": "30-45 minutes per session",
            "tips": [
                "Start slow and gradually increase intensity",
                "Combine exercise with calorie control",
                "Stay consistent rather than doing intense workouts"
            ]
        },
        "obese": {
            "focus": "Safe weight loss and building sustainable habits",
            "exercises": [
                "Walking 20-30 minutes daily",
                "Chair exercises or seated workouts",
                "Water-based activities: Swimming, water aerobics",
                "Gentle yoga or tai chi",
                "Short, frequent activity breaks throughout the day"
            ],
            "duration": "20-30 minutes per session",
            "tips": [
                "Consult healthcare provider before starting",
                "Focus on consistency over intensity",
                "Combine with medical supervision for safety"
            ]
        }
    }
    
    # Age adjustments
    if age < 18:
        recommendations["underweight"]["exercises"].append("Age-appropriate strength training with supervision")
        recommendations["underweight"]["tips"].append("Consult pediatrician before starting exercise program")
    elif age > 65:
        for category in recommendations.values():
            category["exercises"] = [ex.replace("intense", "moderate") for ex in category["exercises"]]
            category["tips"].append("Consult healthcare provider before starting new exercise program")
    
    return recommendations.get(bmi_category, recommendations["normal"])


def get_food_recommendations(bmi_category, goal):
    """
    Get food recommendations based on BMI category and goal.
    
    Args:
        bmi_category: BMI category (underweight, normal, overweight, obese)
        goal: User fitness goal (loss, gain, maintain)
        
    Returns:
        Dictionary with food recommendations
    """
    recommendations = {
        "underweight": {
            "focus": "High-calorie, nutrient-dense foods for healthy weight gain",
            "foods": [
                "Nuts and seeds (almonds, walnuts, chia seeds)",
                "Avocados and healthy fats (olive oil, coconut oil)",
                "Whole grains (brown rice, quinoa, oats)",
                "Lean proteins (chicken, fish, eggs, legumes)",
                "Dairy products (milk, cheese, yogurt)",
                "Fruits and vegetables for nutrients",
                "Nut butters (peanut butter, almond butter)"
            ],
            "meal_ideas": [
                "Smoothie with banana, protein powder, and nut butter",
                "Oatmeal with nuts, seeds, and dried fruits",
                "Salmon with quinoa and avocado",
                "Greek yogurt with granola and honey",
                "Trail mix with nuts and dried fruits"
            ],
            "tips": [
                "Eat calorie-dense foods without feeling overly full",
                "Include healthy fats in every meal",
                "Have snacks between meals",
                "Drink smoothies or shakes for extra calories"
            ]
        },
        "normal": {
            "focus": "Balanced nutrition for maintenance and health",
            "foods": [
                "Lean proteins (chicken, fish, tofu, beans)",
                "Whole grains (brown rice, whole wheat, quinoa)",
                "Fruits and vegetables (variety of colors)",
                "Healthy fats (avocados, nuts, olive oil)",
                "Low-fat dairy or alternatives",
                "Limit processed foods and added sugars"
            ],
            "meal_ideas": [
                "Grilled chicken salad with mixed vegetables",
                "Quinoa bowl with vegetables and lean protein",
                "Fish with brown rice and steamed vegetables",
                "Greek yogurt with fresh fruit",
                "Whole grain toast with avocado"
            ],
            "tips": [
                "Focus on whole, unprocessed foods",
                "Balance macronutrients in each meal",
                "Stay hydrated with water",
                "Include fiber-rich foods for satiety"
            ]
        },
        "overweight": {
            "focus": "Calorie-controlled, nutrient-rich foods for gradual weight loss",
            "foods": [
                "Lean proteins (chicken breast, fish, egg whites)",
                "Non-starchy vegetables (leafy greens, broccoli, zucchini)",
                "Whole grains in moderation (quinoa, brown rice)",
                "Healthy fats in small amounts (avocado, nuts)",
                "Low-calorie condiments and seasonings",
                "Herbal teas and infused water"
            ],
            "meal_ideas": [
                "Large vegetable salad with grilled chicken",
                "Stir-fried vegetables with tofu",
                "Baked fish with steamed vegetables",
                "Greek yogurt with berries",
                "Vegetable soup with lean protein"
            ],
            "tips": [
                "Fill up on low-calorie, high-volume foods",
                "Control portion sizes",
                "Limit added sugars and refined carbs",
                "Include protein with every meal for satiety"
            ]
        },
        "obese": {
            "focus": "Structured meal planning with focus on portion control and nutrients",
            "foods": [
                "Very lean proteins (skinless chicken, fish)",
                "Non-starchy vegetables (unlimited quantities)",
                "Small portions of whole grains",
                "Minimal healthy fats",
                "Sugar-free beverages",
                "Herbal teas and black coffee"
            ],
            "meal_ideas": [
                "Large mixed green salad with minimal dressing",
                "Grilled chicken with unlimited vegetables",
                "Fish with steamed vegetables",
                "Vegetable stir-fry with minimal oil",
                "Clear vegetable soups"
            ],
            "tips": [
                "Focus on vegetable-based meals",
                "Use small plates for portion control",
                "Drink water before meals",
                "Consult healthcare provider for personalized plan"
            ]
        }
    }
    
    return recommendations.get(bmi_category, recommendations["normal"])
