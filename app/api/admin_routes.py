from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.middleware.auth_guard import role_required
from app.services.auth_service import AuthService
from app.services.report_service import ReportService
from app.schemas.attendance_schema import CreateStaffSchema
from marshmallow import ValidationError

admin_bp = Blueprint('admin', __name__)
staff_create_schema = CreateStaffSchema()

@admin_bp.route('/create-staff', methods=['POST'])
@jwt_required()
@role_required('ADMIN')
def create_staff():
    try:
        data = staff_create_schema.load(request.get_json())
    except ValidationError as err:
        error_msg = "; ".join([f"{k}: {', '.join(v)}" for k, v in err.messages.items()])
        return jsonify({"success": False, "error": f"Validation failed: {error_msg}"}), 400

    admin_id = get_jwt_identity()
    
    result, status = AuthService.create_staff(
        admin_id=admin_id,
        name=data.get('name'),
        email=data.get('email'),
        password=data.get('password'),
        department=data.get('department')
    )
    return jsonify(result), status

@admin_bp.route('/reports/all', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def get_all_reports():
    # Admin can view any class report
    class_id = request.args.get('class_id')
    date = request.args.get('date')
    subject = request.args.get('subject')
    
    result, status = ReportService.get_class_report(class_id, date, subject)
    return jsonify(result), status

@admin_bp.route('/staff', methods=['GET'])
@jwt_required()
@role_required('ADMIN')
def get_all_staff():
    from app import mongo
    staff = list(mongo.db.users.find({"role": "STAFF"}, {"password": 0}))
    for s in staff:
        s['_id'] = str(s['_id'])
    return jsonify({"success": True, "staff": staff}), 200
