from requirements.__init__ import create_app
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from the .env file in development
if os.getenv("FLASK_ENV") == "development":
    load_dotenv()

# Create the Flask application instance using the factory function
app = create_app()

# Get CORS origins from environment variable, fallback to default origins if not defined
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:8080", "https://www.v97-cems.com")
if allowed_origins:
    allowed_origins = allowed_origins.split(",")  # Split into a list of origins if multiple are provided

# Allow specific origins for production or localhost for development
CORS(app, origins=allowed_origins)

# If the script is run directly, start the app
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_ENV") == "development")



# backend/app.py
# from requirements.__init__ import create_app
# from flask_cors import CORS


# # Create the Flask application instance using the factory function
# app = create_app()

# # Allow all origins (can be restricted in production)
# CORS(app, origins="http://localhost:3000")

# # If the script is run directly, start the app
# if __name__ == "__main__":
#     app.run(debug=True)
