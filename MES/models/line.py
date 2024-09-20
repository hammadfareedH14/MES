from db import db
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship

class LineModel(CommonModel, SurrogatePK):
    __tablename__ = "line"
    name = db.Column(db.String(100), nullable=False)
    # foreign key 
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False) 
    # relationship 
    shops = relationship("ShopModel", back_populates="lines") # shop
    stations = relationship("StationModel", back_populates="lines") # station 
