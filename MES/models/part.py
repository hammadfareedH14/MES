from db import db 
from models.abstract import CommonModel,SurrogatePK
# from sqlalchemy.orm import relationship


class PartModel(CommonModel, SurrogatePK):
    __tablename__="part"
    name = db.Column(db.String(200), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
