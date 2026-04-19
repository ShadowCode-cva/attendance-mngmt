from flask import Blueprint, jsonify, request
from app import mongo
from bson import ObjectId

metadata_bp = Blueprint('metadata', __name__)

@metadata_bp.route('/years', methods=['GET'])
def get_years():
    years = list(mongo.db.years.find({}, {"_id": 1, "name": 1, "code": 1}))
    for y in years:
        y["_id"] = str(y["_id"])
    return jsonify({"success": True, "years": years}), 200

@metadata_bp.route('/departments', methods=['GET'])
def get_departments():
    depts = list(mongo.db.departments.find({}, {"_id": 1, "name": 1, "code": 1}))
    for d in depts:
        d["_id"] = str(d["_id"])
    return jsonify({"success": True, "departments": depts}), 200

@metadata_bp.route('/subjects', methods=['GET'])
def get_subjects():
    subs = list(mongo.db.subjects.find({}, {"_id": 1, "name": 1, "code": 1}))
    for s in subs:
        s["_id"] = str(s["_id"])
    return jsonify({"success": True, "subjects": subs}), 200

@metadata_bp.route('/class', methods=['GET'])
def get_class():
    year_id = request.args.get('year_id')
    dept_id = request.args.get('dept_id')
    
    if not year_id or not dept_id:
        return jsonify({"success": False, "message": "Missing year_id or dept_id"}), 400
        
    cls = mongo.db.classes.find_one({
        "year_id": ObjectId(year_id) if isinstance(year_id, str) else year_id,
        "dept_id": ObjectId(dept_id) if isinstance(dept_id, str) else dept_id
    })
    
    if not cls:
        return jsonify({"success": False, "message": "Class not found"}), 404
        
    cls["_id"] = str(cls["_id"])
    cls["year_id"] = str(cls["year_id"])
    cls["dept_id"] = str(cls["dept_id"])
    
    return jsonify({"success": True, "class_data": cls}), 200

@metadata_bp.route('/students', methods=['GET'])
def get_students():
    class_id = request.args.get('class_id')
    if not class_id:
        return jsonify({"success": False, "message": "Missing class_id"}), 400
        
    students = list(mongo.db.students.find({"class_id": ObjectId(class_id) if isinstance(class_id, str) else class_id}, {"_id": 1, "name": 1, "reg_no": 1}))
    for s in students:
        s["_id"] = str(s["_id"])
    return jsonify({"success": True, "students": students}), 200
