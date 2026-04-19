from marshmallow import Schema, fields, validate

class AttendanceRecordSchema(Schema):
    student_id = fields.Str(required=True)
    status = fields.Str(required=True, validate=validate.OneOf(["PRESENT", "ABSENT"]))

class MarkAttendanceSchema(Schema):
    class_id = fields.Str(required=True)
    subject = fields.Str(required=True)
    hour = fields.Int(required=True, validate=validate.Range(min=1, max=8))
    date = fields.Str(required=True) # Format validation can be added
    records = fields.List(fields.Nested(AttendanceRecordSchema), required=True)

class CreateStaffSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
    department = fields.Str(required=False)
