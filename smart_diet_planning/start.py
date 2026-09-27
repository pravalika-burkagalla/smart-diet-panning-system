#!/usr/bin/env python3
"""
Quick start script for Smart Diet Planning Flask application.
Run this to start the application.
"""
import os
import sys

# Change to project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)
sys.path.insert(0, project_dir)

# Import and initialize the Flask app
import app

print("[INFO] Initializing database...")
app.init_db()

print("[INFO] Starting Smart Diet Planning application...")
print("[INFO] Open http://localhost:5000 in your browser")
print("[INFO] Press Ctrl+C to stop the server\n")

# Run Flask application
app.app.run(host='0.0.0.0', debug=False, port=5000, use_reloader=False)
