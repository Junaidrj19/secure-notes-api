from marshmallow import Schema, fields, validate

class NoteSchema(Schema):
    title = fields.Str(
        required = True,
        validate = validate.Length(min=3,max=50)
    )
    content = fields.Str(
        required = True,
    )
    created_at = fields.DateTime(dump_only=True)

class NoteUpdateSchema(Schema):
    title = fields.Str()
    content = fields.Str()

class NoteResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
