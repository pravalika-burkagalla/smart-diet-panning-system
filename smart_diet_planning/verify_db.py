import os
import sqlite3

os.chdir(r'd:\smart_diet_planning')

# Import the app to run init_db
import app
app.init_db()

print("[OK] Database initialized")

# Verify the new schema
conn = sqlite3.connect('food.db')
cur = conn.cursor()

# Check food_items table
try:
    cur.execute("SELECT COUNT(*) FROM food_items")
    count = cur.fetchone()[0]
    print(f"[OK] Food items table: {count} items loaded")
    
    # Show sample items from each meal type
    cur.execute("SELECT food_name, calories, meal_type FROM food_items LIMIT 1")
    print(f"[OK] Sample item: {cur.fetchone()}")
    
    # Count by meal type
    cur.execute("SELECT meal_type, COUNT(*) FROM food_items GROUP BY meal_type")
    print("[OK] Items by meal type:")
    for meal_type, cnt in cur.fetchall():
        print(f"    - {meal_type}: {cnt} items")
except Exception as e:
    print(f"[ERROR] food_items: {e}")

# Check user_metrics table
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_metrics'")
    if cur.fetchone():
        print("[OK] User metrics table created")
    else:
        print("[WARNING] User metrics table not found")
except Exception as e:
    print(f"[ERROR] user_metrics check: {e}")

conn.close()
print("\n[SUCCESS] Database setup complete!")
