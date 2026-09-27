import sqlite3

conn = sqlite3.connect(r'd:\smart_diet_planning\food.db')
cur = conn.cursor()

print("=" * 80)
print("COMPREHENSIVE FOOD DATABASE SUMMARY")
print("=" * 80)

# Get all foods
cur.execute("SELECT food_name, calories, protein, carbs, fats, meal_type FROM food_items ORDER BY meal_type")
foods = cur.fetchall()

current_meal = None
for food_name, cal, protein, carbs, fats, meal_type in foods:
    if meal_type != current_meal:
        if current_meal is not None:
            print()
        print(f"\n{meal_type.upper()} ({meal_type})")
        print("-" * 80)
        current_meal = meal_type
    
    print(f"  {food_name:40} | {cal:3}cal | P:{protein:5.1f}g | C:{carbs:5.1f}g | F:{fats:5.1f}g")

print("\n" + "=" * 80)
print(f"Total Foods: {len(foods)}")

# Summary stats
cur.execute("SELECT meal_type, COUNT(*), AVG(calories), AVG(protein) FROM food_items GROUP BY meal_type ORDER BY meal_type")
print("\nMeal Type Summary:")
print("-" * 80)
for meal_type, count, avg_cal, avg_protein in cur.fetchall():
    print(f"  {meal_type:10}: {count:2} items  |  Avg Calories: {avg_cal:6.0f}  |  Avg Protein: {avg_protein:5.1f}g")

print("=" * 80)
conn.close()
