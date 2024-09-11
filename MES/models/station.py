from db import db 
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship

class StationModel(CommonModel, SurrogatePK):
    __tablename__ = "station"
    name = db.Column(db.String(100), nullable=False)
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'), nullable=False)
    lines = relationship("LineModel", back_populates="stations")
    locations = relationship("LocationModel", back_populates="stations")



