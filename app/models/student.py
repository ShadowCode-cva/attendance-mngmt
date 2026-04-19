from bson import ObjectId
from app import mongo

class Student:
    @staticmethod
    def create_student(reg_no, name, gender, class_id, contact_email=None):
        student = {
            "reg_no": reg_no,
            "name": name,
            "gender": gender, # MALE, FEMALE, OTHER
            "class_id": ObjectId(class_id) if isinstance(class_id, str) else class_id,
            "contact_info": {
                "email": contact_email
            },
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        return mongo.db.students.insert_one(student)

    @staticmethod
    def find_by_reg_no(reg_no):
        return mongo.db.students.find_one({"reg_no": reg_no})

    @staticmethod
    def find_by_class(class_id):
        query_id = ObjectId(class_id) if isinstance(class_id, str) else class_id
        return list(mongo.db.students.find({"class_id": query_id}))
