from app import mongo

class SubjectService:
    @staticmethod
    def get_all_subjects():
        subjects = mongo.db.subjects.find()
        return [s['name'] for s in subjects]

    @staticmethod
    def is_valid_subject(subject_name):
        return mongo.db.subjects.find_one({"name": subject_name}) is not None

    @staticmethod
    def add_subject(name, code=None):
        if mongo.db.subjects.find_one({"name": name}):
            return {"success": False, "message": "Subject already exists"}, 400
        
        mongo.db.subjects.insert_one({
            "name": name,
            "code": code
        })
        return {"success": True, "message": "Subject added successfully"}, 201
