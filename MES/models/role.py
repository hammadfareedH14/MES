from models.abstract import CommonModel,SurrogatePK
from db import db

class RoleModel(CommonModel, SurrogatePK):
    __tablename__ = "role"
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

 # Define relationship
    users = db.relationship('UserModel', back_populates='role')
