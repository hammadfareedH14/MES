from db import db
from models.abstract import CommonModel, SurrogatePK

class OperationModel(CommonModel, SurrogatePK):
    __tablename__ = 'operation'

    start_timestamp = db.Column(db.DateTime, nullable=False)
    complete_timestamp = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False, default="not start")
    mark_status = db.Column(db.String, nullable=False,default="ok")
    comment = db.Column(db.JSON, nullable=False) 
    
# Work Instruction and User fields
    work_instruction_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)


