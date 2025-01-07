# backend/create_users.py

from requirements.__init__ import db
from models import Role, User
from werkzeug.security import generate_password_hash

# Create default roles
admin_role = Role(name='Admin')
hr_role = Role(name='HR')
ta_admin_role = Role(name='TA-Admin')
it_admin_role = Role(name='IT-Admin')

# Add roles to the session and commit
db.session.add(admin_role)
db.session.add(hr_role)
db.session.add(ta_admin_role)
db.session.add(it_admin_role)
db.session.commit()

# Create default users
admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('adminroot'), role=admin_role)
hr_user = User(username='hr', email='hr@example.com', password=generate_password_hash('hrroot'), role=hr_role)

# Add users to the session and commit
db.session.add(admin_user)
db.session.add(hr_user)
db.session.commit()

print("Default roles and users added.")
