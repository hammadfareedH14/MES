from db import db
from models.abstract import CommonModel, SurrogatePK
from sqlalchemy.orm import relationship


class NodeModel(CommonModel, SurrogatePK):
    __tablename__ = 'node'

    current_station_id = db.Column(db.String, db.ForeignKey('station.id'), nullable=False)
    next_station_id = db.Column(db.String, db.ForeignKey('station.id'), nullable=False)
    route_id = db.Column(db.String, db.ForeignKey('route.id'), nullable=False)
    is_start = db.Column(db.Boolean, default=False)
    is_end = db.Column(db.Boolean, default=False)
    
    # Relationships
    current_station = relationship("StationModel", foreign_keys=[current_station_id], back_populates="current_nodes")
    next_station = relationship("StationModel", foreign_keys=[next_station_id], back_populates="next_nodes")
    route = relationship("RouteModel", back_populates="nodes")
