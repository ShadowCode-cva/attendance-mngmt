from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middleware.auth_guard import role_required
from app.services.attendance_service import AttendanceService
from app.services.report_service import ReportService
from app.services.auth_service import AuthService
from app.schemas.attendance_schema import MarkAttendanceSchema
from marshmallow import ValidationError

staff_bp = Blueprint('staff', __name__)
mark_schema = MarkAttendanceSchema()

@staff_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return AuthService.login(data.get('email'), data.get('password'))

@staff_bp.route('/mark', methods=['POST'])
@jwt_required()
@role_required('STAFF')
def mark_attendance():
    try:
        data = mark_schema.load(request.get_json())
    except ValidationError as err:
        error_msg = "; ".join([f"{k}: {', '.join(v)}" for k, v in err.messages.items()])
        return jsonify({"success": False, "error": f"Validation failed: {error_msg}"}), 400

    staff_id = get_jwt_identity()
    
    result, status = AttendanceService.mark_class_attendance(
        staff_id=staff_id,
        class_id=data.get('class_id'),
        subject=data.get('subject'),
        hour=data.get('hour'),
        date_str=data.get('date'),
        student_records=data.get('records')
    )
    return jsonify(result), status

@staff_bp.route('/report/class', methods=['GET'])
@jwt_required()
@role_required('STAFF')
def get_class_report():
    class_id = request.args.get('class_id')
    date = request.args.get('date')
    subject = request.args.get('subject')
    
    result, status = ReportService.get_class_report(class_id, date, subject)
    return jsonify(result), status

@staff_bp.route('/student/<reg_no>', methods=['GET'])
@jwt_required()
@role_required('STAFF')
def get_student_detail(reg_no):
    # Staff can see a student's full monthly report
    now = datetime.utcnow()
    year = int(request.args.get('year', now.year))
    month = int(request.args.get('month', now.month))
    
    result, status = ReportService.get_student_monthly_report(reg_no, year, month)
    return jsonify(result), status
