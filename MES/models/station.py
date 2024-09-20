from db import db 
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship

class StationModel(CommonModel, SurrogatePK):
    __tablename__ = "station"
    name = db.Column(db.String(100), nullable=False)
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'), nullable=False)

    # Relationships
    lines = relationship("LineModel", back_populates="stations")
    locations = relationship("LocationModel", back_populates="stations")
    current_nodes = relationship("NodeModel", foreign_keys='NodeModel.current_station_id', back_populates="current_station")
    next_nodes = relationship("NodeModel", foreign_keys='NodeModel.next_station_id', back_populates="next_station")



