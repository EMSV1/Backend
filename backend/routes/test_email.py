from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Configuration
app.config['MAIL_SERVER'] = 'smtpout.secureserver.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

# Initialize Flask-Mail
mail = Mail(app)

@app.route('/send_test_email')
def send_test_email():
    try:
        msg = Message(
            subject="Test Email",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=["cems1812@gmail.com"],  # Replace with the recipient's email
            body="This is a test email sent from Flask using smtpout.secureserver.net."
        )
        mail.send(msg)
        return "Test email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"

if __name__ == "__main__":
    app.run(debug=True)
