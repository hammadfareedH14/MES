from db import db 
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)
from flask_login import (
    UserMixin,
    LoginManager,
    login_required,
    current_user,
    logout_user,
    login_user,
)

class UserModel(CommonModel, SurrogatePK, UserMixin):
    __tablename__ = "user"
    username = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    disabled = db.Column(db.Boolean, default=False)  
    work_location_ids = db.Column(db.JSON,db.ForeignKey('location.id'),default=[])  

  # Define relationships
    role = relationship('RoleModel', back_populates='users')
    locations = relationship('LocationModel',back_populates='users')

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.passwordhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
