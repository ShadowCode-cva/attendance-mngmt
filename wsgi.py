import os
import sys
from app import create_app

# Use 'prod' environment config if FLASK_ENV is set to production, else fallback to 'dev'
env = os.getenv('FLASK_ENV', 'prod')

try:
    # Create the application instance
    app = create_app(env)
    print(f"[v0] Flask app created successfully with environment: {env}", file=sys.stderr)
except Exception as e:
    print(f"[v0] CRITICAL ERROR: Failed to create Flask app: {str(e)}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

if __name__ == "__main__":
    # This block is ignored by Gunicorn/Vercel, but useful if run directly
    app.run(debug=False)

