import os
os.chdir(r'd:\smart_diet_planning')
import app
app.init_db()
print("[INFO] Database initialized")
print("[INFO] Starting Flask app on http://127.0.0.1:5000")
print("[INFO] Press Ctrl+C to stop\n")
app.app.run(host='0.0.0.0', debug=False, port=5000, use_reloader=False)
