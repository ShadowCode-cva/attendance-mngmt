import os
import sys
from flask import send_from_directory

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'prod'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    # If the path looks like an API call, let the blueprints handle it
    # (Though Vercel rewrites should handle this, this is a fallback)
    if path.startswith('api/'):
        return {"error": "Not Found"}, 404
        
    # Otherwise, try to serve from the root directory
    if path == "" or path == "/":
        return send_from_directory(project_root, 'index.html')
    
    return send_from_directory(project_root, path)
