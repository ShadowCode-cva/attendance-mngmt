import os
import sys

# Use 'prod' environment config if FLASK_ENV is set to production, else fallback to 'dev'
env = os.getenv('FLASK_ENV', 'prod')

try:
    from app import create_app
    # Create the application instance
    app = create_app(env)
    print(f"[v0] Flask app created successfully with environment: {env}", file=sys.stderr)
except Exception as e:
    print(f"[v0] CRITICAL ERROR: Failed to create Flask app: {str(e)}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    # Still raise to fail fast, but ensure app is defined
    app = None
    raise

# Ensure app is available at module level for Vercel
if app is None:
    raise RuntimeError("Failed to initialize Flask application")

if __name__ == "__main__":
    # This block is ignored by Gunicorn/Vercel, but useful if run directly
    app.run(debug=False)

