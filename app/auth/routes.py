from flask import Blueprint, request, jsonify
from app.config import db
from app.models import User
from flask_bcrypt import Bcrypt
from app import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.auth.schemas import CreateUserSchema
from app.models import TokenBlocklist
from app import JWTManager

auth_bp = Blueprint('auth_bp',__name__)

@auth_bp.route('/register',methods=['POST'])
def register():
    """
    Register a new user
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
    """
    data = request.get_json()
    user_schema = CreateUserSchema()
    errors = user_schema.validate(data)
    
    if errors:
        return jsonify(errors), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error":"Email already registered"}),400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username,email=email,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User registered successfully"}),201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: junaid@example.com
            password:
              type: string
              example: strongpassword123
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({"token": access_token}), 200



@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Logout user (revoke JWT)
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: Successfully logged out
      401:
        description: Unauthorized
    """
    jti = get_jwt()["jti"] 
    db.session.add(TokenBlocklist(jti=jti))
    db.session.commit()
    return jsonify(msg="Successfully logged out"), 200
