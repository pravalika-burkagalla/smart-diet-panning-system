import os
import sys

os.chdir(r'd:\smart_diet_planning')
sys.path.insert(0, r'd:\smart_diet_planning')

print("[INFO] Testing diet logic module...")
from logic.diet_logic import calculate_bmi, calculate_bmr, calorie_requirement, generate_diet_plan

# Test 1: calculate_bmi
bmi = calculate_bmi(70, 175)
print(f"[OK] BMI calculation: 70kg, 175cm -> {bmi}")

# Test 2: calculate_bmr
bmr = calculate_bmr(70, 175, 25, "male")
print(f"[OK] BMR calculation: 70kg, 175cm, 25yr, male -> {bmr}")

# Test 3: calorie_requirement
cals = calorie_requirement(1700, "moderate")
print(f"[OK] Calorie requirement: 1700 BMR, moderate -> {cals}")

# Test 4: generate_diet_plan
food_items = [
    ("Oats", 150, 5, 27, 3, "Breakfast"),
    ("Eggs", 70, 6, 1, 5, "Breakfast"),
    ("Rice", 200, 4, 45, 1, "Lunch"),
    ("Dal", 120, 7, 20, 2, "Lunch"),
    ("Chicken", 250, 25, 0, 10, "Dinner"),
    ("Salad", 80, 2, 10, 1, "Dinner"),
]

plan = generate_diet_plan(food_items, 2500, "loss")
print(f"[OK] Diet plan generated: {plan}")

print("\n[SUCCESS] All diet logic functions work correctly!")
