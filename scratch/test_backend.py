import requests
import json
import time
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment
load_dotenv()
BASE_URL = "http://127.0.0.1:5000/api"
MONGO_URI = os.getenv("MONGO_URI")

def test_backend():
    print("--- STARTING FULL BACKEND TEST ---")
    
    # 1. Admin Login
    print("\n[1] Testing Admin Login...")
    login_data = {"email": "admin@college.edu", "password": "admin123"}
    resp = requests.post(f"{BASE_URL}/staff/login", json=login_data)
    if resp.status_code != 200:
        print("FAIL: Admin login failed")
        return
    admin_token = resp.json()['access_token']
    print("SUCCESS: Admin logged in.")

    # 2. Staff Login (Using seeded staff)
    print("\n[2] Testing Staff Login...")
    staff_login = {"email": "staff@college.edu", "password": "staff123"}
    resp = requests.post(f"{BASE_URL}/staff/login", json=staff_login)
    staff_token = resp.json()['access_token']
    staff_headers = {"Authorization": f"Bearer {staff_token}"}
    print("SUCCESS: Staff logged in.")

    # 3. Mark Attendance
    print("\n[3] Testing Attendance Marking with Real Data...")
    
    # Fetch real IDs from Atlas
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    
    student1 = db.students.find_one({"reg_no": "71222403002"})
    student2 = db.students.find_one({"reg_no": "71222403003"})
    
    if not student1 or not student2:
        print("FAIL: Could not find real students in database. Run seed_db.py first.")
        return
        
    class_id = str(student1['class_id'])
    
    attendance_data = {
        "class_id": class_id,
        "subject": "Mathematics",
        "hour": 1,
        "date": time.strftime("%Y-%m-%d"),
        "records": [
            {"student_id": str(student1['_id']), "status": "PRESENT"},
            {"student_id": str(student2['_id']), "status": "PRESENT"}
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/staff/mark", json=attendance_data, headers=staff_headers)
    print(f"RESPONSE: {resp.json().get('message', 'No message')}")
    
    # 4. Check Class Report
    print("\n[4] Testing Class Report (Staff)...")
    report_params = {
        "class_id": class_id,
        "date": time.strftime("%Y-%m-%d"),
        "subject": "Mathematics"
    }
    resp = requests.get(f"{BASE_URL}/staff/report/class", params=report_params, headers=staff_headers)
    if resp.status_code != 200:
        print(f"FAIL: Class report failed with status {resp.status_code}")
        print(f"TEXT: {resp.text}")
        return
        
    report = resp.json()
    print(f"Class: {report.get('class_name')}")
    print(f"Total Strength: {report.get('total_strength')}")
    print(f"Absentees: {len(report.get('absentees', []))}")

    # 5. Check Student Public Report
    print("\n[5] Testing Student Public Report...")
    resp = requests.get(f"{BASE_URL}/student/attendance/71222403002")
    data = resp.json()
    print(f"Student: {data.get('student_name')}")
    print(f"Percentage: {data.get('percentage')}%")

    print("\n--- TEST COMPLETE ---")

if __name__ == "__main__":
    test_backend()
