from db import db
import uuid
import os
from werkzeug import secure_filename

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Text, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    verified = db.Column(db.Boolean, nullable=False, default=False)
    size_used = db.Column(db.Float, default=0.0)
    size_limit = db.Column(db.Float,default=500000)
    files = db.relationship('FileModel', lazy='dynamic')
    location = db.Column(db.Text, nullable=False)


    def __init__(self, email, password):

        self.id = str(uuid.uuid3(uuid.NAMESPACE_DNS, email))
        self.email = email
        self.password = password
        self.location = 'storage/{}'.format(secure_filename(self.id))

        try:
            os.makedirs(self.location)
        except:
            pass

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete(self):

        db.session.delete(self)
        db.session.commit()

    def get_location(self):
        return self.location

    def get_size_used(self):
        return self.size_used

    def get_size_limit(self):
        return self.size_limit
        

    def is_verified(self):

        return self.verified

    def get_all_file_names(self):

        return {
            'files': [file_.name for file_ in self.files.all()]
        }
    def list_all_files(self):

        i = 1
        ret = {}
        for file in self.files.all():
            val = 'file{}'.format(i)
            ret[val] = file.dict_repr()
            i+=1
        return ret

    @staticmethod
    def find_by_email(email):
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(_id):
        return UserModel.query.filter_by(id=_id).first()



