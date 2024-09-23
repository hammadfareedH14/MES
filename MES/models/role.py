from models.abstract import CommonModel,SurrogatePK
from db import db
from sqlalchemy.orm import relationship

class RoleModel(CommonModel, SurrogatePK):
    __tablename__ = "role"
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)

 # Relationship
    users = relationship('UserModel', back_populates='role')
