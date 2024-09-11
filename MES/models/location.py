from db import db
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship 

class LocationModel(CommonModel, SurrogatePK):
    __tablename__ = "location"
    name = db.Column(db.String(100), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=False)
    stations = relationship("StationModel", back_populates="locations")
    