from db import db 
from models.abstract import CommonModel,SurrogatePK
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

class User(CommonModel, SurrogatePK, UserMixin):
    __tablename__ = "users"
    username = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    emailaddress = db.Column(db.String(255), nullable=False)
    passwordhash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.passwordhash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)