from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os
import csv
from logic.diet_logic import calculate_bmi, calculate_bmr, calorie_requirement, generate_diet_plan_improved, get_age_group_data, get_bmi_category, get_exercise_recommendations, get_food_recommendations

app = Flask(__name__)
app.secret_key = 'smart_diet_planner_secret_key_2026'

def get_food_items():
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()
    cursor.execute("SELECT food_name, calories, protein, carbs, fats, meal_type FROM food_items")
    items = cursor.fetchall()
    conn.close()
    return items


def map_category_to_meal_type(category, food_name=None):
    name_lower = (food_name or "").strip().lower()
    cat_lower = (category or "").strip().lower()

    if any(term in name_lower for term in ["breakfast", "oat", "cereal", "toast", "pancake", "omelet", "smoothie", "morning"]):
        return "Breakfast"
    if any(term in name_lower for term in ["salad", "sandwich", "bowl", "taco", "rice", "vegetable", "burger", "wrap", "pizza"]):
        return "Lunch"
    if any(term in name_lower for term in ["dinner", "steak", "fish", "soup", "pasta", "casserole", "roast", "meat", "chicken", "beef", "pork", "shrimp"]):
        return "Dinner"
    if any(term in name_lower for term in ["snack", "nut", "yogurt", "bar", "juice", "fruit", "dried", "cookie", "cake", "pie", "dessert"]):
        return "Snack"

    if any(term in cat_lower for term in ["breakfast", "cereal", "oat", "pancake"]):
        return "Breakfast"
    if any(term in cat_lower for term in ["salad", "sandwich", "lunch", "bowl", "taco", "meat", "poultry"]):
        return "Lunch"
    if any(term in cat_lower for term in ["dinner", "steak", "fish", "soup", "pasta", "casserole"]):
        return "Dinner"
    if any(term in cat_lower for term in ["snack", "nut", "yogurt", "bar", "juice", "fruit", "dried", "ice cream", "dessert"]):
        return "Snack"

    return "Snack"


def import_food_data_from_csv(csv_path):
    if not os.path.exists(csv_path):
        return 0

    imported = 0
    conn = sqlite3.connect("food.db")
    cursor = conn.cursor()

    with open(csv_path, mode="r", encoding="utf-8", errors="replace") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            food_name = row.get("food_name", "").strip()
            if not food_name:
                continue

            calories = row.get("calories") or "0"
            protein = row.get("protein") or "0"
            carbs = row.get("carbs") or "0"
            fats = row.get("fat") or row.get("fats") or "0"
            category = row.get("category", "")
            meal_type = map_category_to_meal_type(category)

            try:
                calories_val = float(calories)
                protein_val = float(protein)
                carbs_val = float(carbs)
                fats_val = float(fats)
            except ValueError:
                continue

            # Keep existing entries from DB if they already exist
            cursor.execute("SELECT 1 FROM food_items WHERE food_name = ?", (food_name,))
            if cursor.fetchone():
                continue

            cursor.execute(
                "INSERT INTO food_items (food_name, calories, protein, carbs, fats, meal_type) VALUES (?, ?, ?, ?, ?, ?)",
                (food_name, calories_val, protein_val, carbs_val, fats_val, meal_type)
            )
            imported += 1

    conn.commit()
    conn.close()
    return imported


def init_db():
    # Create SQLite DB from database.sql if it doesn't exist
    if not os.path.exists("food.db"):
        if os.path.exists("database.sql"):
            conn = sqlite3.connect("food.db")
            cursor = conn.cursor()
            with open("database.sql", "r", encoding="utf-8") as f:
                sql = f.read()
            cursor.executescript(sql)
            conn.commit()
            conn.close()
        else:
            # create empty table as fallback
            conn = sqlite3.connect("food.db")
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS food_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    food_name TEXT,
                    calories INTEGER,
                    protein REAL,
                    carbs REAL,
                    fats REAL,
                    meal_type TEXT
                )
                """
            )
            conn.commit()
            conn.close()

    # If dataset exists at the path provided by the user, load more food data
    user_csv = r"D:\My Pics\archive_data\Food_Nutrition_Dataset.csv"
    imported_count = import_food_data_from_csv(user_csv)
    if imported_count > 0:
        print(f"Imported {imported_count} new food items from {user_csv}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    age = int(request.form["age"])
    gender = request.form["gender"]
    height = float(request.form["height"])  # Now properly handles float
    weight = float(request.form["weight"])  # Now properly handles float
    activity = request.form["activity"]
    goal = request.form["goal"]

    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age, gender)
    calories = calorie_requirement(bmr, activity)

    food_items = get_food_items()

    # Use the centralized BMI category logic from diet_logic
    bmi_category_display = get_bmi_category(bmi, age).capitalize()
    bmi_category_logic = get_bmi_category(bmi, age)

    diet_plan = generate_diet_plan_improved(
        food_items, calories, goal, bmi_category_logic, age, gender
    )
    
    age_group_data = get_age_group_data(age)
    exercise_recommendations = get_exercise_recommendations(bmi_category_logic, age, activity)
    food_recommendations = get_food_recommendations(bmi_category_logic, goal)

    # Store all data in session
    session['user_data'] = {
        'bmi': bmi,
        'bmr': bmr,
        'calories': calories,
        'diet_plan': diet_plan,
        'age_group': age_group_data,
        'bmi_category': bmi_category_display,
        'bmi_category_logic': bmi_category_logic,
        'goal': goal,
        'exercises': exercise_recommendations,
        'foods': food_recommendations
    }

    return redirect(url_for('bmi_results'))

@app.route("/bmi")
def bmi_results():
    if 'user_data' not in session:
        return redirect(url_for('index'))
    
    data = session['user_data']
    return render_template(
        "result_bmi.html",
        bmi=data['bmi'],
        bmr=data['bmr'],
        calories=data['calories'],
        goal=data.get('goal'),
        bmi_category=data['bmi_category'],
        diet_plan=data['diet_plan']
    )

@app.route("/age-group")
def age_group():
    if 'user_data' not in session:
        return redirect(url_for('index'))
    
    data = session['user_data']
    return render_template("result_age.html", age_group=data['age_group'])

@app.route("/exercise")
def exercise_rec():
    if 'user_data' not in session:
        return redirect(url_for('index'))
    
    data = session['user_data']
    return render_template("result_exercise.html", exercises=data['exercises'])

@app.route("/food")
def food_rec():
    if 'user_data' not in session:
        return redirect(url_for('index'))
    
    data = session['user_data']
    return render_template("result_food.html", foods=data['foods'])

@app.route("/meal-plan")
def meal_plan():
    if 'user_data' not in session:
        return redirect(url_for('index'))
    
    data = session['user_data']
    return render_template(
        "result_meal.html",
        diet_plan=data['diet_plan'],
        goal=data['goal'],
        bmi_category=data['bmi_category'],
        age_group=data['age_group']
    )

if __name__ == "__main__":
    init_db()
    app.run(debug=True)

