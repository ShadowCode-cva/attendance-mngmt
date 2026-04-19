from datetime import datetime
from app import mongo

class Attendance:
    @staticmethod
    def init_indexes():
        # Compound unique index: student + subject + hour + date
        mongo.db.attendance.create_index(
            [("student_id", 1), ("subject", 1), ("hour", 1), ("date", 1)],
            unique=True
        )
        # Index for class reports
        mongo.db.attendance.create_index([("class_id", 1), ("date", 1)])

    @staticmethod
    def mark_attendance(records):
        """
        records: list of attendance documents
        """
        if not records:
            return None
        return mongo.db.attendance.insert_many(records)

    @staticmethod
    def get_attendance_query(query):
        return list(mongo.db.attendance.find(query))
