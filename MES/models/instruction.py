from db import db
from models.abstract import CommonModel, SurrogatePK
from sqlalchemy.orm import relationship

class InstructionModel(CommonModel, SurrogatePK):
    __tablename__ = 'instruction'

    # Fields in the Instruction model
    description = db.Column(db.String, nullable=True)  
    category_id = db.Column(db.String, db.ForeignKey('category.id'), nullable=True)
    work_location_id = db.Column(db.String, db.ForeignKey('work_location.id'), nullable=True)
    

    # Parts relationship (assuming one-to-many)
    parts = relationship('PartModel', backref='instruction', lazy='dynamic')


