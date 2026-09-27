import sys
import os
os.chdir(r'd:\smart_diet_planning')
print("Python Version:", sys.version)
print("Working Dir:", os.getcwd())
print()
print("Attempting to import app...")
try:
    import app
    print("[OK] app imported successfully")
except Exception as e:
    print(f"[ERROR] Failed to import app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\nAttempting to run Flask app...")
try:
    app.app.run(debug=True, port=5000)
except Exception as e:
    print(f"[ERROR] Flask failed to start: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
