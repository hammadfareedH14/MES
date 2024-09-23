from db import db
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship 

class LocationModel(CommonModel, SurrogatePK):
    __tablename__ = "location"
    name = db.Column(db.String(100), nullable=False)
    
    # ForeignKey
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)

#   Relationship
    stations = relationship("StationModel", back_populates="locations") 
    users = relationship('UserModel', back_populates='locations') 
    
