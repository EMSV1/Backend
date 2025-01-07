from werkzeug.utils import secure_filename
import os
from config import Config

# Utility function for allowed file types (only PDF for job descriptions)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Function for saving uploaded PDFs
def save_pdf(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filename
    return None


# utils.py

from flask_jwt_extended import get_jwt_identity
from models import User

def check_role(required_role):
    """
    Check if the currently authenticated user has the required role.
    Raises a Forbidden error if the user does not have the required role.
    """
    current_user_email = get_jwt_identity()  # Get the email of the currently logged-in user
    user = User.query.filter_by(email=current_user_email).first()  # Fetch user from the database by email
    
    if not user:
        raise Exception("User not found")
    
    if user.role.role_name != required_role:  # Check if the user has the required role
        raise PermissionError(f"User does not have the {required_role} role.")

