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
    # Pure API server — no static files (Vercel CDN serves public/)
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.json_provider_class = MongoJSONProvider
    app.json = MongoJSONProvider(app)

    # Logging Configuration (Clean format)
    import logging
    import os
    logging.basicConfig(level=logging.INFO, 
                        format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%H:%M:%S')
    
    logger = logging.getLogger(__name__)
    
    # Check for required environment variables
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        logger.warning("MONGO_URI environment variable is not set")
    
    jwt_secret = os.getenv('JWT_SECRET_KEY')
    if not jwt_secret:
        logger.warning("JWT_SECRET_KEY environment variable is not set")

    # Initialize Extensions
    try:
        mongo.init_app(app)
    except Exception as e:
        logger.error(f"Failed to initialize MongoDB: {str(e)}")
    
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Global Error Handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled Exception: {str(e)}", exc_info=True)
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

    @app.route('/health')
    def health():
        mongo_connected = False
        try:
            # Try to ping MongoDB
            mongo.db.command('ping')
            mongo_connected = True
        except Exception as e:
            logger.warning(f"MongoDB connection check failed: {str(e)}")
        
        return {
            "status": "healthy", 
            "mongo_connected": mongo_connected,
            "environment": config_name
        }, 200 if mongo_connected else 503

    @app.route('/config-check')
    def config_check():
        """Debug endpoint to check configuration (remove in production)"""
        return {
            "mongo_uri_set": bool(os.getenv('MONGO_URI')),
            "jwt_secret_set": bool(os.getenv('JWT_SECRET_KEY')),
            "secret_key_set": bool(os.getenv('SECRET_KEY')),
            "debug_mode": app.debug,
            "flask_env": os.getenv('FLASK_ENV', 'not set')
        }, 200

    return app
