import os, sqlite3
os.chdir(r"d:\smart_diet_planning")
print('CWD:', os.getcwd())
import app
app.init_db()
print('Checked init_db()')
print('food.db exists:', os.path.exists('food.db'))
conn = sqlite3.connect('food.db')
cur = conn.cursor()
try:
    cur.execute("SELECT food_name, calories FROM food_items LIMIT 5")
    rows = cur.fetchall()
    print('sample rows:', rows)
except Exception as e:
    print('query error:', e)
finally:
    conn.close()
