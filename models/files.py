import enum
from db import db
import uuid
from werkzeug import secure_filename

class FileModel(db.Model):

    __tablename__ = 'files'

    id = db.Column(db.Text, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    name = db.Column(db.String, nullable=False)
    saved_as = db.Column(db.Text,nullable=False)
    size = db.Column(db.Float, nullable=False, default=0.0)

    description = db.Column(db.String, default='')
    owner_id = db.Column(db.Text, db.ForeignKey('users.id'))

    deleted = db.Column(db.Boolean,default=True)
    deleted_at = db.Column(db.DateTime,nullable=True)

    def __init__(self,name,saved_as,owner_id,
                 description='',
                 _size=0.0, filetype='None'):

        self.id = str(uuid.uuid3(uuid.NAMESPACE_DNS, '{}{}'.format(owner_id,name)))
        self.name = name
        self.saved_as = saved_as
        self.owner_id = owner_id
        self.description = description
        self.size = _size

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def array_repr(self):

        return [self.name,self.size,str(self.updated_on),self.description]

    def dict_repr(self):
        return {
        "Name":self.name,
        "Size":self.size,
        "Updated_On": str(self.updated_on),
        "Description":self.description
        }

    @staticmethod
    def find_by_owner(owner_id):
        return FileModel.query.filter_by(owner_id=owner_id).all()

    @staticmethod
    def find_by_owner_name(owner_id,name):
        return FileModel.query.filter_by(owner_id=owner_id,name=name).first()


