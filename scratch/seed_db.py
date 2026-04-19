import os
import sys
from datetime import datetime

# Ensure local project is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, mongo, bcrypt
from app.models.user import User
from app.models.student import Student
from app.models.attendance import Attendance

def seed_db():
    app = create_app('dev')
    with app.app_context():
        print("--- CLEANING DATABASE ---")
        mongo.db.users.delete_many({})
        mongo.db.students.delete_many({})
        mongo.db.classes.delete_many({})
        mongo.db.attendance.delete_many({})
        mongo.db.subjects.delete_many({})

        # Initialize Attendance Indexes
        Attendance.init_indexes()

        # 0. Create Master Subjects
        mongo.db.subjects.insert_many([
            {"name": "Mathematics", "code": "MATH101"},
            {"name": "Data Structures", "code": "CS201"},
            {"name": "Computer Networks", "code": "CS301"}
        ])
        print("Created Master Subjects")

        # 1. Create Admin
        admin_id = User.create_user("Admin User", "admin@college.edu", "admin123", "ADMIN").inserted_id
        print(f"Created Admin: admin@college.edu / admin123")

        # 2. Create Staff
        staff_id = User.create_user("Dr. Smith", "staff@college.edu", "staff123", "STAFF").inserted_id
        print(f"Created Staff: staff@college.edu / staff123")

        # 3. Create Academic Structure
        years = mongo.db.years.insert_many([
            {"name": "1st Year", "code": 1},
            {"name": "2nd Year", "code": 2},
            {"name": "3rd Year", "code": 3},
            {"name": "4th Year", "code": 4}
        ]).inserted_ids

        depts = mongo.db.departments.insert_many([
            {"name": "CSE", "code": "CSE"},
            {"name": "IT", "code": "IT"},
            {"name": "AGRI", "code": "AGRI"}
        ]).inserted_ids

        # 4. Create "2nd Year CSE" Class
        class_id = mongo.db.classes.insert_one({
            "year_id": years[1],
            "dept_id": depts[0],
            "name": "B.Tech CS - Year 2",
            "total_strength": 46
        }).inserted_id
        print(f"Created Class: B.Tech CS - Year 2 (ID: {class_id})")

        # 5. Create 46 Students (Real Data)
        student_data = [
            ("71222403002", "Abhro Kanth S", "MALE"), ("71222403003", "Abirami G", "FEMALE"),
            ("71222403004", "Adaikalasamy V", "MALE"), ("71222403005", "Adhimoolam A", "MALE"),
            ("71222403006", "Akalya E", "FEMALE"), ("71222403007", "Akash P", "MALE"),
            ("71222403008", "Aravindh P", "MALE"), ("71222403010", "Ashika S M", "FEMALE"),
            ("71222403013", "Bharath R", "MALE"), ("71222403014", "Castro Jenifer S", "FEMALE"),
            ("71222403015", "Dhanalakshmi B", "FEMALE"), ("71222403016", "Dhanush P", "MALE"),
            ("71222403017", "Dharani P", "FEMALE"), ("71222403019", "Ganesh M", "MALE"),
            ("71222403021", "Harish V", "MALE"), ("71222403022", "Jaiaravindhan C M", "MALE"),
            ("71222403023", "Kalaiarasan N", "MALE"), ("71222403024", "Kathir Manikandan P", "MALE"),
            ("71222403026", "Kishore Kannan B", "MALE"), ("71222403027", "Kishore P", "MALE"),
            ("71222403028", "Kishore S", "MALE"), ("71222403029", "Kishore Selvakumar", "MALE"),
            ("71222403031", "Maha Rakesh K", "MALE"), ("71222403032", "Mahalakshmi G", "FEMALE"),
            ("71222403034", "Mohanraj T", "MALE"), ("71222403035", "Mugilan M", "MALE"),
            ("71222403036", "Nadhiya N", "FEMALE"), ("71222403037", "Nagoor Sheik Mydeen P", "MALE"),
            ("71222403038", "Navaneetha Nagarajan L", "MALE"), ("71222403039", "Navin B", "MALE"),
            ("71222403040", "Poopathi C", "MALE"), ("71222403041", "Rashiya S", "FEMALE"),
            ("71222403043", "Rathna Nithi M", "FEMALE"), ("71222403044", "Rithanya M", "FEMALE"),
            ("71222403045", "Sakthivel A", "MALE"), ("71222403046", "Sanju B", "MALE"),
            ("71222403047", "Santhosh R", "MALE"), ("71222403050", "Sathishkumar M", "MALE"),
            ("71222403053", "Siva K", "MALE"), ("71222403054", "Sivarajan S", "MALE"),
            ("71222403055", "Sudhahar S", "MALE"), ("71222403056", "Sureka K", "FEMALE"),
            ("71222403057", "Susmitha V", "FEMALE"), ("71222403059", "Thamaraiselvan M", "MALE"),
            ("71222403061", "Vishal K", "MALE"), ("71222403063", "Yogeswaran N", "MALE")
        ]

        students = []
        for reg, name, gender in student_data:
            email = name.lower().replace(' ', '.') + "@college.edu"
            phone = f"+91-98765-{reg[-5:]}"
            students.append({
                "reg_no": reg,
                "name": name,
                "gender": gender,
                "email": email,
                "phone": phone,
                "class_id": class_id
            })
        
        mongo.db.students.insert_many(students)
        print(f"Successfully Seeded 46 Students into 2nd Year CSE")

if __name__ == "__main__":
    seed_db()
