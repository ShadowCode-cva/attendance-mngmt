import os
from app import create_app

# Use 'prod' environment config if FLASK_ENV is set to production, else fallback to 'dev'
env = os.getenv('FLASK_ENV', 'prod')

# Create the application instance
app = create_app(env)

if __name__ == "__main__":
    # This block is ignored by Gunicorn, but useful if run directly
    app.run()
