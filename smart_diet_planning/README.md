# Smart Diet Planning Application

A Flask-based web application that calculates personalized diet plans based on user health metrics including BMI, BMR (Basal Metabolic Rate), and daily calorie requirements.

## Features

- **BMI Calculator**: Calculate Body Mass Index based on height and weight
- **BMR Calculator**: Calculate Basal Metabolic Rate using age, gender, height, and weight
- **Calorie Requirements**: Compute daily calorie needs based on activity level
- **Personalized Diet Plans**: Generate meal recommendations based on fitness goals
- **Web Interface**: Easy-to-use form for entering health metrics
- **SQLite Database**: Store and manage food item information

## Project Structure

```
smart_diet_planning/
├── app.py                      # Main Flask application
├── start.py                    # Quick start script
├── requirements.txt            # Python dependencies
├── database.sql               # Database schema and sample data
├── food.model                 # SQLAlchemy model definitions
├── logic/
│   ├── __init__.py
│   └── diet_logic.py          # Core diet calculation functions
├── templates/
│   ├── index.html             # User input form
│   └── result.html            # Results display page
├── static/
│   ├── style.css              # CSS styling
│   └── js.script              # JavaScript functionality
├── food.db                    # SQLite database (auto-created)
└── PROJECT_STATUS.md          # Detailed status report
```

## Requirements

- Python 3.8+
- Virtual Environment (recommended)
- Flask 3.0.0
- SQLite3 (included with Python)

## Installation

### 1. Clone or Extract Project
```bash
cd smart_diet_planning
```

### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using the Start Script (Recommended)
```bash
python start.py
```

### Method 2: Direct Python Execution
```bash
python app.py
```

The application will:
1. Initialize the SQLite database with sample food items
2. Start the Flask development server
3. Display: `Running on http://127.0.0.1:5000`

## Usage

1. **Open in Browser**: Navigate to `http://localhost:5000` or `http://127.0.0.1:5000`

2. **Enter Your Details**:
   - Age (years)
   - Gender (Male/Female)
   - Height (centimeters)
   - Weight (kilograms)
   - Activity Level (Sedentary, Light, Moderate, Active, Very Active)
   - Goal (Weight Loss, Weight Gain, Maintain)

3. **Submit Form**: Click "Generate Plan"

4. **View Results**:
   - Your BMI and category
   - Your BMR (calories burned at rest)
   - Daily calorie requirement
   - Personalized meal suggestions for Breakfast, Lunch, and Dinner

## Sample Data

The application comes with 6 sample food items:
- **Breakfast**: Oats (150 cal), Eggs (70 cal)
- **Lunch**: Rice (200 cal), Dal (120 cal)
- **Dinner**: Chicken (250 cal), Salad (80 cal)

## Diet Calculations

### BMI Formula
```
BMI = weight (kg) / (height (m))²
```

### BMR Formula (Mifflin-St Jeor)
- **Male**: 10×weight + 6.25×height - 5×age + 5
- **Female**: 10×weight + 6.25×height - 5×age - 161

### Daily Calorie Requirement
```
Daily Calories = BMR × Activity Factor

Activity Factors:
- Sedentary: 1.2
- Light: 1.375
- Moderate: 1.55
- Active: 1.725
- Very Active: 1.9
```

## Customization

### Add More Foods
Edit `database.sql` and add rows to the INSERT statement:
```sql
INSERT INTO food_items (food_name, calories, protein, carbs, fats, meal_type)
VALUES ("Chicken Breast", 165, 31, 0, 3.6, "Lunch");
```

Then delete `food.db` to regenerate from the SQL file.

### Modify Styling
Edit `static/style.css` to customize the appearance

### Change Port
In `app.py` or `start.py`, change:
```python
app.run(port=5000)  # Change 5000 to your desired port
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### "Address already in use" (Port 5000)
- The port is occupied by another process
- Change port in `start.py`: `app.run(port=8000)`

### Database not found
- Delete `food.db` and restart (it will be recreated)
- Check that `database.sql` exists in the project directory

### Templates not found
- Ensure `templates/` folder exists with `index.html` and `result.html`
- Verify file permissions

## Testing

The project includes test scripts:
```bash
# Test diet calculation logic
python test_logic.py

# Check Flask server (requires server running)
python test_flask.ps1  # PowerShell version
```

## Deployment

For production deployment:

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Waitress (Windows-friendly)
```bash
pip install waitress
waitress-serve --port=5000 app:app
```

## Future Enhancements

- User authentication and saved meal preferences
- Advanced charting with matplotlib
- Machine learning for personalized recommendations
- Mobile app integration
- Nutritionist consultation scheduling
- Meal tracking and progress monitoring

## License

Open source project - feel free to modify and distribute

## Support

For issues or questions, refer to PROJECT_STATUS.md for detailed information.
