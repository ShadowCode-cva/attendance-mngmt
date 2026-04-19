import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, mongo

app = create_app('dev')
with app.app_context():
    all_depts = ["CSE", "IT", "AGRI", "AIDS", "BME", "CYBER SECURITY", "MECH", "EEE", "ECE", "AERO"]
    
    existing = {d['code'] for d in mongo.db.departments.find({}, {"code": 1})}
    
    to_insert = []
    for d in all_depts:
        if d not in existing:
            to_insert.append({"name": d, "code": d})
            
    if to_insert:
        mongo.db.departments.insert_many(to_insert)
        print(f"Inserted missing departments: {[d['code'] for d in to_insert]}")
    else:
        print("All departments already exist.")
