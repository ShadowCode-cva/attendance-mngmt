from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from .config import config_by_name
from .utils.helpers import MongoJSONProvider

mongo = PyMongo()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_name='dev'):
    # Point static_folder to the frontend directory
    app = Flask(__name__, static_folder='../frontend', static_url_path='/')
    app.config.from_object(config_by_name[config_name])
    app.json_provider_class = MongoJSONProvider
    app.json = MongoJSONProvider(app)

    # Initialize Extensions
    mongo.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Logging Configuration (Clean format)
    import logging
    logging.basicConfig(level=logging.INFO, 
                        format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%H:%M:%S')

    # Global Error Handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled Exception: {str(e)}")
        return {"success": False, "error": "INTERNAL_SERVER_ERROR", "message": "An unexpected error occurred."}, 500

    @app.errorhandler(404)
    def not_found(e):
        return {"success": False, "error": "NOT_FOUND", "message": "Resource not found."}, 404

    @app.errorhandler(403)
    def forbidden(e):
        return {"success": False, "error": "FORBIDDEN", "message": "Access denied."}, 403

    # Register Blueprints
    from .api.admin_routes import admin_bp
    from .api.staff_routes import staff_bp
    from .api.student_routes import student_bp
    from .api.metadata_routes import metadata_bp

    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(staff_bp, url_prefix='/api/staff')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(metadata_bp, url_prefix='/api/metadata')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/health')
    def health():
        return {"status": "healthy"}, 200

    return app
