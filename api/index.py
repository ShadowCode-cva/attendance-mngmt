import os
import sys

# Add the project root to Python path so 'app' package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app(os.getenv('FLASK_ENV', 'prod'))
