from pymongo import ReplaceOne
from datetime import datetime
from bson import ObjectId
from app import mongo
from app.models.attendance import Attendance
from app.models.student import Student

from app.services.subject_service import SubjectService

class AttendanceService:
    @staticmethod
    def mark_class_attendance(staff_id, class_id, subject, hour, date_str, student_records):
        """
        student_records: list of {student_id, status}
        """
        # 1. Subject Validation
        if not SubjectService.is_valid_subject(subject):
            return {"success": False, "message": f"Invalid subject: {subject}"}, 400

        # 2. Date Validation (Only today allowed)
        current_date = datetime.utcnow().strftime('%Y-%m-%d')
        if date_str != current_date:
            return {"success": False, "message": "Attendance can only be marked for the current day"}, 403

        if not (1 <= hour <= 8):
            return {"success": False, "message": "Hour must be between 1 and 8"}, 400

        # 2. Fetch all valid students for this class once
        students_in_class = {str(s['_id']): s for s in Student.find_by_class(class_id)}
        
        timestamp = datetime.utcnow()
        bulk_operations = []

        for record in student_records:
            s_id = record['student_id']
            status = record['status']
            
            if status not in ['PRESENT', 'ABSENT']:
                continue # Skip invalid status
            
            if s_id not in students_in_class:
                continue # Security: Student must belong to the class
                
            filter_query = {
                "student_id": ObjectId(s_id),
                "subject": subject,
                "hour": hour,
                "date": date_str
            }
            
            update_doc = {
                "student_id": ObjectId(s_id),
                "class_id": ObjectId(class_id),
                "student_gender": students_in_class[s_id]['gender'],
                "subject": subject,
                "hour": hour,
                "date": date_str,
                "status": status,
                "marked_by": ObjectId(staff_id),
                "timestamp": timestamp
            }
            
            # Prepare Bulk Replace Operation (Upsert)
            bulk_operations.append(
                ReplaceOne(filter_query, update_doc, upsert=True)
            )

        if not bulk_operations:
            return {"success": False, "message": "No valid records to process"}, 400

        try:
            # Atomic Bulk Write
            mongo.db.attendance.bulk_write(bulk_operations)
            return {"success": True, "message": "Attendance processed successfully"}, 200
        except Exception as e:
            # The global error handler in __init__.py will catch unexpected errors
            # but we can log specific DB issues here if needed
            raise e
