import sqlite3

# Test direct SQL execution
conn = sqlite3.connect(':memory:')
cur = conn.cursor()

with open(r'd:\smart_diet_planning\database.sql', 'r', encoding='utf-8') as f:
    sql = f.read()

print(f"SQL Length: {len(sql)}")
print("Attempting to execute SQL...")

try:
    cur.executescript(sql)
    print("[OK] SQL executed successfully")
    
    cur.execute("SELECT COUNT(*) FROM food_items")
    count = cur.fetchone()[0]
    print(f"[OK] Food items count: {count}")
    
except Exception as e:
    print(f"[ERROR] {e}")
    print(f"Error type: {type(e)}")

conn.close()
