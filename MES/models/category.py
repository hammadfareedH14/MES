from db import db 
from enum import Enum
from models.abstract import CommonModel,SurrogatePK
# from sqlalchemy.orm import relationship

class Type(Enum):
    """
    Type model:
    - WORK: work type
    - PART: part type 
    """
    WORK = "work"
    PART = "part"


class CategoryModel(CommonModel, SurrogatePK):
    __tablename__ = "category"
    name = db.Column(db.String(100), nullable=False)
    _type = db.Column(db.Enum(Type), nullable=False)
    