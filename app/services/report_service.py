from app import mongo
from bson import ObjectId

class ReportService:
    @staticmethod
    def get_student_monthly_report(reg_no, year, month):
        # First find student to get _id
        student = mongo.db.students.find_one({"reg_no": reg_no})
        if not student:
            return {"message": "Student not found"}, 404

        start_date = f"{year}-{month:02d}-01"
        # Simple end date logic (next month)
        next_month = month + 1 if month < 12 else 1
        next_year = year if month < 12 else year + 1
        end_date = f"{next_year}-{next_month:02d}-01"

        pipeline = [
            { 
                "$match": { 
                    "student_id": ObjectId(student['_id']), 
                    "date": { "$gte": start_date, "$lt": end_date } 
                } 
            },
            {
                "$group": {
                    "_id": "$student_id",
                    "total_sessions": { "$sum": 1 },
                    "present_count": { "$sum": { "$cond": [{ "$eq": ["$status", "PRESENT"] }, 1, 0] } },
                    "absent_count": { "$sum": { "$cond": [{ "$eq": ["$status", "ABSENT"] }, 1, 0] } }
                }
            },
            {
                "$project": {
                    "student_name": { "$literal": student['name'] },
                    "total_sessions": 1,
                    "present_count": 1,
                    "absent_count": 1,
                    "percentage": { 
                        "$cond": [
                            { "$eq": ["$total_sessions", 0] },
                            0,
                            { "$multiply": [ { "$divide": ["$present_count", "$total_sessions"] }, 100 ] }
                        ]
                    }
                }
            }
        ]

        result = list(mongo.db.attendance.aggregate(pipeline))
        if not result:
            return {
                "student_name": student['name'],
                "total_sessions": 0,
                "present_count": 0,
                "absent_count": 0,
                "percentage": 0
            }, 200
            
        return result[0], 200

    @staticmethod
    def get_class_report(class_id, date_str, subject):
        # First get class details
        class_info = mongo.db.classes.find_one({"_id": ObjectId(class_id)})
        if not class_info:
            return {"message": "Class not found"}, 404

        pipeline = [
            { "$match": { "class_id": ObjectId(class_id), "date": date_str, "subject": subject } },
            {
                "$facet": {
                    "gender_stats": [
                        {
                            "$group": {
                                "_id": "$student_gender",
                                "present": { "$sum": { "$cond": [{ "$eq": ["$status", "PRESENT"] }, 1, 0] } }
                            }
                        }
                    ],
                    "absentees": [
                        { "$match": { "status": "ABSENT" } },
                        {
                            "$lookup": {
                                "from": "students",
                                "localField": "student_id",
                                "foreignField": "_id",
                                "as": "details"
                            }
                        },
                        { "$unwind": { "path": "$details", "preserveNullAndEmptyArrays": True } },
                        { "$project": { "name": "$details.name", "reg_no": "$details.reg_no" } }
                    ],
                    "metadata": [
                        { "$limit": 1 },
                        {
                            "$lookup": {
                                "from": "users",
                                "localField": "marked_by",
                                "foreignField": "_id",
                                "as": "staff"
                            }
                        },
                        { "$unwind": { "path": "$staff", "preserveNullAndEmptyArrays": True } },
                        { "$project": { "staff_name": "$staff.name", "timestamp": 1 } }
                    ]
                }
            },
            {
                "$project": {
                    "class_name": { "$literal": class_info['name'] },
                    "total_strength": { "$literal": class_info['total_strength'] },
                    "gender_stats": 1,
                    "absentees": 1,
                    "metadata": 1
                }
            }
        ]

        result = list(mongo.db.attendance.aggregate(pipeline))
        if not result:
             return {
                "class_name": class_info['name'],
                "total_strength": class_info['total_strength'],
                "gender_stats": [],
                "absentees": [],
                "metadata": []
            }, 200
            
        return result[0], 200
