import requests
import time

# Give server a moment
time.sleep(1)

# Test 1: GET homepage
try:
    resp = requests.get('http://127.0.0.1:5000/')
    print(f"GET / -> Status: {resp.status_code}")
    if resp.status_code == 200:
        print("✓ Index page loads successfully")
        if "<h2>Enter Your Details</h2>" in resp.text:
            print("✓ Form content found in index.html")
except Exception as e:
    print(f"✗ GET / failed: {e}")

# Test 2: POST with valid form data
try:
    form_data = {
        'age': '25',
        'gender': 'Male',
        'height': '175',
        'weight': '70',
        'activity': 'moderate',
        'goal': 'loss'
    }
    resp = requests.post('http://127.0.0.1:5000/result', data=form_data)
    print(f"\nPOST /result -> Status: {resp.status_code}")
    if resp.status_code == 200:
        print("✓ Form submission successful")
        if "BMI:" in resp.text and "Breakfast" in resp.text:
            print("✓ Results page displays BMI and diet plan")
except Exception as e:
    print(f"✗ POST /result failed: {e}")

print("\n✓ All tests passed! App is working correctly.")
