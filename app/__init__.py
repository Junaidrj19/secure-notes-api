from flask import Flask
from app.config import db,init_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.models import TokenBlocklist
from flasgger import Swagger


bcrypt = Bcrypt()
jwt = JWTManager()

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Secure Notes API",
        "description": "JWT protected API",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header. Example: Bearer <token>"
        }
    }
}

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None 

def create_app():
    app = Flask(__name__)
    init_app(app)

    bcrypt.init_app(app)
    jwt.init_app(app)

    Swagger(app,template=swagger_template)   

    from app.auth.routes import auth_bp
    from app.notes.routes import note_bp

    app.register_blueprint(note_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app