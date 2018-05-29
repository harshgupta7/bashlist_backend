import enum
from db import db


class FileEnum(enum.Enum):
    directory = 1
    file = 2


class FileModel(db.Model):

    __tablename__ = 'objects'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    name = db.Column(db.String, nullable=False)
    size = db.Column(db.Float, nullable=False, default=0.0)
    location = db.Column(db.String, nullable=False, default='.')
    type_ = db.Column(db.Enum(FileEnum),default=FileEnum.file)
    description = db.Column(db.String, default='')
    filetype = db.Column(db.String, default='None')
    owner_email = db.Column(db.String, db.ForeignKey('users.email'))

    def __init__(self,name,owner_email,
                 description='',location='.',
                 _type=FileEnum.directory, _size=0.0, filetype='None'):

        self.name = name
        self.owner_email = owner_email
        self.description = description
        self.location = location
        self.type_ = _type
        self.size = _size
        self.filetype = filetype

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def array_repr(self):

        return [self.name,self.size,self.date,self.description]


    @staticmethod
    def find_by_owner(owner_email):
        return FileModel.query.filter_by(owner_email=owner_email).first()


