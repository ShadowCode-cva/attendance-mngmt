import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

# Vercel looks exactly for a variable named 'app'
app = create_app(os.getenv('FLASK_ENV', 'prod'))
