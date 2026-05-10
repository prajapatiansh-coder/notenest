from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)
    avatar = fields.Str(dump_only=True)

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    subject = fields.Str(required=True)
    semester = fields.Str(required=True)
    description = fields.Str()
    filename = fields.Str(dump_only=True)
    uploaded_at = fields.DateTime(dump_only=True)
    downloads = fields.Int(dump_only=True)
    ai_summary = fields.Str(dump_only=True)
    uploader = fields.Nested(UserSchema, dump_only=True)
