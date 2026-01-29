from flask import Blueprint, request, jsonify
from app.config import db
from app.models import Note
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.notes.schemas import NoteSchema, NoteResponseSchema, NoteUpdateSchema
from marshmallow import ValidationError

note_bp = Blueprint('note_bp',__name__)

@note_bp.route('/notes',methods=['POST'])
@jwt_required()
def create_note():
    """
    Create a note
    ---
    tags:
      - Notes
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: My first note
            content:
              type: string
              example: Created from Swagger
    responses:
      200:
        description: Note created successfully
      404:
        description: Note not found
      401:
        description: Unauthorized
    """
    try:
        data = NoteSchema().load(request.get_json())
    except ValidationError as err:
        return {"errors":err.messages}, 400
    
    current_user_id = get_jwt_identity()

    title = data.get('title')
    content = data.get('content')

    new_note = Note(title=title,content=content,user_id=current_user_id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({
        "message":"Note created succesfully",
        "note" : {
            "id" : new_note.id,
            "title" : new_note.title,
            "content" : new_note.content,
            "created_at" : new_note.created_at
        }
    }), 201

@note_bp.route('/notes',methods=['GET'])
@jwt_required()
def get_notes():
    """
    Get all notes for current user
    ---
    tags:
      - Notes
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Note fetched successfully
      404:
        description: Note not found
      401:
        description: Unauthorized
    """
    current_user_id = get_jwt_identity()

    notes = Note.query.filter_by(user_id=current_user_id).all()

    return jsonify({
        "notes": NoteResponseSchema(many=True).dump(notes)
    }), 200

@note_bp.route('/notes/<int:id>',methods=['PUT'])
@jwt_required()
def update_note(id):
    """
    Update a note
    ---
    tags:
      - Notes
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the note to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
          properties:
            title:
              type: string
              example: My Updated Note
            content:
              type: string
              example: Updated from Swagger
    responses:
      200:
        description: Note Updated successfully
      404:
        description: Note not found
      401:
        description: Unauthorized
    """
    try:
        data = NoteUpdateSchema().load(request.get_json())
    except ValidationError as err:
        return {"errors":err.messages}, 400

    current_user_id = get_jwt_identity()

    user_note = Note.query.filter_by(id=id,user_id=current_user_id).first()
    if not user_note:
        return jsonify({"message":"Note not found"}), 404

    if "title" in data:
        user_note.title = data["title"]
    if "content" in data:
        user_note.content = data["content"]
    db.session.commit()

    return jsonify({"message":"Note updated successfully"}), 200

@note_bp.route('/notes/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_note(id):
    """
    Delete a note
    ---
    tags:
      - Notes
    security:
      - Bearer: []
    parameters:
      - name: id
        in: path
        required: true
        type: integer
        example: 1
    responses:
      200:
        description: Note deleted successfully
      404:
        description: Note not found
      401:
        description: Unauthorized
    """
    current_user_id = get_jwt_identity()
    note = Note.query.filter_by(id=id,user_id=current_user_id).first()

    if not note:
        return jsonify({"error":"Note not found"}), 400

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message":"Note deleted successfully"})