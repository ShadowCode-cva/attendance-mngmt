from flask import Blueprint, request, jsonify
from app.services.report_service import ReportService
from datetime import datetime

student_bp = Blueprint('student', __name__)

@student_bp.route('/attendance/<reg_no>', methods=['GET'])
def get_monthly_attendance(reg_no):
    # Default to current month/year
    now = datetime.utcnow()
    year = int(request.args.get('year', now.year))
    month = int(request.args.get('month', now.month))
    
    result, status = ReportService.get_student_monthly_report(reg_no, year, month)
    return jsonify(result), status
