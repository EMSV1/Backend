from requirements.__init__ import create_app
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from the .env file in development
if os.getenv('FLASK_ENV') == 'development':
    load_dotenv()

# Create the Flask application instance using the factory function
app = create_app()

# Allow specific origins for production or localhost for development
CORS(app, origins=os.getenv("CORS_ORIGINS", "http://localhost:3000"))

# If the script is run directly, start the app
if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_ENV') == 'development')












# # backend/app.py
# from requirements.__init__ import create_app
# from flask_cors import CORS


# # Create the Flask application instance using the factory function
# app = create_app()

# # Allow all origins (can be restricted in production)
# CORS(app, origins="http://localhost:3000")

# # If the script is run directly, start the app
# if __name__ == "__main__":
#     app.run(debug=True)
