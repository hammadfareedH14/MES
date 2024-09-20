from db import db
from models.abstract import CommonModel, SurrogatePK

class DataCaptureModel(CommonModel, SurrogatePK):
    __tablename__ = 'datacapture'

    action = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    work_operation_id = db.Column(db.Integer, db.ForeignKey("operation.id"), nullable=False)
