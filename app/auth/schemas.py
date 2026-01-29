from marshmallow import Schema, fields, validate

class CreateUserSchema(Schema):
    username = fields.Str(
        required = True,
        validate = validate.Length(min=3,max=50)
    )
    email = fields.Str(
        required = True,
        error_messages = {"required": "Email is required"}
    )
    password = fields.Str(
        required = True,
        validate = validate.Length(min=6),
        load_only = True
    )