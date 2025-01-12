from datetime import datetime, timezone
from requirements.__init__ import (
    db,
)  # Import db from __init__.py, which avoids circular imports


def get_current_utc_time():
    """
    Returns the current UTC time. This is used to ensure all timestamps are in UTC.
    """
    return datetime.now(timezone.utc)


class Role(db.Model):
    __tablename__ = "roles"

    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.role_name}>"

    def to_dict(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name,
            "description": self.description,
        }


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    # Foreign Key referencing Role Table
    role_id = db.Column(db.Integer, db.ForeignKey("roles.role_id"), nullable=False)

    role = db.relationship("Role", backref=db.backref("users", lazy=True))

    def __repr__(self):
        return f"<User {self.email}, Role {self.role.role_name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "role_id": self.role_id,
            "role": self.role.to_dict(),  # Use the to_dict method for the related Role
        }


class Requirement(db.Model):
    __tablename__ = "requirements"

    requirement_id = db.Column(db.Integer, primary_key=True)
    business_unit = db.Column(db.String(100))
    resource_requirement = db.Column(db.String(100))
    job_description = db.Column(db.String(1000))
    resource_type = db.Column(db.String(50))
    business_title = db.Column(db.String(100))
    vector_title = db.Column(db.String(100))
    comments = db.Column(db.Text)
    department = db.Column(db.String(100))
    created_date = db.Column(db.DateTime, default=get_current_utc_time)
    last_modified_date = db.Column(
        db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time
    )

    def to_dict(self):
        return {
            "requirement_id": self.requirement_id,
            "business_unit": self.business_unit,
            "resource_requirement": self.resource_requirement,
            "job_description": self.job_description,
            "resource_type": self.resource_type,
            "business_title": self.business_title,
            "vector_title": self.vector_title,
            "comments": self.comments,
            "department": self.department,
            "created_date": self.created_date.isoformat(),
            "last_modified_date": self.last_modified_date.isoformat(),
        }


class RequirementApproval(db.Model):
    __tablename__ = "requirement_approval"

    approval_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)

    requirement_id = db.Column(
        db.Integer, db.ForeignKey("requirements.requirement_id"), nullable=False
    )
    approval_status = db.Column(db.String(50))
    approved_by = db.Column(db.String(100))
    last_modified_date = db.Column(
        db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time
    )


class InterviewStatus(db.Model):
    __tablename__ = "interview_status"

    interview_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=True)
    requirement_id = db.Column(
        db.Integer, db.ForeignKey("requirements.requirement_id"), nullable=False
    )
    interview_status = db.Column(db.String(50))  # Pending, Hold, Approved, Rejected
    interview_round = db.Column(db.String(50))  # Preliminary, Final, HR Round
    candidate_name = db.Column(db.String(100), nullable=True)  # New field
    interviewer_name = db.Column(db.String(100), nullable=True)  # New field
    interview_date = db.Column(db.DateTime, nullable=True)  # New field
    last_modified_date = db.Column(
        db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time
    )

    def to_dict(self):
        return {
            'requirement_id': self.requirement_id,
            'interview_status': self.interview_status,
            'interview_round': self.interview_round,
            'candidate_name': self.candidate_name,
            'interviewer_name': self.interviewer_name,
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'last_modified_date': self.last_modified_date.isoformat(),
        }


class Joining(db.Model):
    __tablename__ = "joining"

    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    emp_email_id = db.Column(db.String(100))
    employee_address = db.Column(db.String(255))
    business_unit = db.Column(db.String(100))
    business_title = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))  # Full Time / Contract
    contact_number = db.Column(db.String(50))
    reporting_manager = db.Column(db.String(100))
    employment_status = db.Column(db.String(50))  # Active / Inactive
    created_date = db.Column(db.DateTime, default=get_current_utc_time)
    last_modified_date = db.Column(
        db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time
    )

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "emp_email_id": self.emp_email_id,
            "employee_address": self.employee_address,
            "business_unit": self.business_unit,
            "business_title": self.business_title,
            "resource_type": self.resource_type,
            "contact_number": self.contact_number,
            "reporting_manager": self.reporting_manager,
            "employment_status": self.employment_status,
            "created_date": self.created_date.isoformat(),
            "last_modified_date": self.last_modified_date.isoformat(),
        }


class ITAssets(db.Model):
    __tablename__ = "it_assets"

    asset_id = db.Column(
        db.Integer, primary_key=True
    )  # The primary key for the IT assets
    employee_id = db.Column(db.Integer, nullable=False)
    laptop = db.Column(db.String(100), nullable=False)
    monitor = db.Column(db.String(100), nullable=False)
    wired_keyboard = db.Column(db.String(100), nullable=False)
    wired_mouse = db.Column(db.String(100), nullable=False)
    wireless_mouse = db.Column(db.String(100), nullable=False)
    airtel_dongle = db.Column(db.String(100), nullable=False)
    id_card = db.Column(db.String(100), nullable=False)
    employment_status = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=get_current_utc_time)
    last_modified_date = db.Column(
        db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time
    )

    def __init__(
        self,
        employee_id,
        laptop,
        monitor,
        wired_keyboard,
        wired_mouse,
        wireless_mouse,
        airtel_dongle,
        id_card,
        employment_status,
    ):
        self.employee_id = employee_id
        self.laptop = laptop
        self.monitor = monitor
        self.wired_keyboard = wired_keyboard
        self.wired_mouse = wired_mouse
        self.wireless_mouse = wireless_mouse
        self.airtel_dongle = airtel_dongle
        self.id_card = id_card
        self.employment_status = employment_status

    def __repr__(self):
        return f"<ITAsset {self.asset_id}>"


class SoftwareLicense(db.Model):
    __tablename__ = "software_licenses"

    license_id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(
        db.Integer, db.ForeignKey("joining.employee_id"), nullable=False
    )
    created_date = db.Column(db.DateTime, default=get_current_utc_time)
    last_modified_date = db.Column(
        db.DateTime, default=get_current_utc_time, onupdate=get_current_utc_time
    )
    dynamic_attributes = db.relationship(
        "LicenseAttribute", backref="software_license", lazy=True
    )


class LicenseAttribute(db.Model):
    __tablename__ = "license_attributes"

    attribute_id = db.Column(db.Integer, primary_key=True)
    license_id = db.Column(
        db.Integer, db.ForeignKey("software_licenses.license_id"), nullable=False
    )
    attribute_name = db.Column(db.String(100))
    attribute_value = db.Column(db.String(255))
