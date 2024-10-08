from db import db 
from models.abstract import CommonModel,SurrogatePK


class RouteModel(CommonModel, SurrogatePK):
    __tablename__ = "route"
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300), nullable=False)

# Relationship
    nodes = db.relationship("NodeModel", back_populates="route")
    parts = relationship('PartModel', back_populates='routes')  
