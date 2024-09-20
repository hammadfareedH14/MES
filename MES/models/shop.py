from db import db 
from models.abstract import CommonModel,SurrogatePK
from sqlalchemy.orm import relationship

class ShopModel(CommonModel, SurrogatePK):
    __tablename__="shop"
    name = db.Column(db.String(200), nullable=False)
    
    lines = relationship("LineModel", back_populates="shops")
    

   
