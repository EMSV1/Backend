from models import Role
from requirements.__init__ import db


def create_default_roles():
    roles = ['Super-Admin', 'Admin', 'HR', 'TA-Admin', 'IT-Admin']
    
    for role_name in roles:
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            new_role = Role(role_name=role_name, description=f"Role for {role_name}")
            db.session.add(new_role)
            db.session.commit()
