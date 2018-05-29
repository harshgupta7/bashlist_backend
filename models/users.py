from db import db


class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    verified = db.Column(db.Boolean, nullable=False, default=False)
    size_used = db.Column(db.Float, default=0.0)
    pub_keys = db.relationship('PubKeyModel', lazy='dynamic')
    files = db.relationship('FileModel', lazy='dynamic')

    def __init__(self, email, password):

        self.email = email
        self.password = password

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete(self):

        db.session.delete(self)
        db.session.commit()

    def is_verified(self):

        return self.verified

    def get_all_keys(self):

        return {
            'keys': [key.__str__() for key in self.pub_keys.all()]
        }

    def get_all_file_names(self):

        return {
            'files': [file_.name for file_ in self.files.all()]
        }
    def list_all_files(self):
        return{
            'files':[file_.array_repr() for file_ in self.files.all()]
        }

    @staticmethod
    def find_by_email(email):
        return UserModel.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(_id):
        return UserModel.query.filter_by(id=_id).first()



