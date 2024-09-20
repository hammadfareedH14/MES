
from db import db 
from models.abstract import CommonModel,SurrogatePK
# from sqlalchemy.orm import relationship


class FileModel(CommonModel,SurrogatePK):
    __tablename__ = 'files'

    filename = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)

    def get_by_filename(filename):
        return FileModel.query.filter_by(filename=filename).first()
