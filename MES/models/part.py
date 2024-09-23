from db import db  
from models.abstract import CommonModel, SurrogatePK
from sqlalchemy.orm import relationship
class PartModel(CommonModel, SurrogatePK):
    __tablename__ = "part"
    description = db.Column(db.String(200), nullable=False)
    number = db.Column(db.Integer, nullable=False)

    # ForeignKey
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)  
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False) 
    
    # Relationships
    categories = relationship('CategoryModel', back_populates='parts')  
    routes = relationship('RouteModel', back_populates='parts')  
