from db import db


class PubKeyModel(db.Model):

    __tablename__ = 'pubkeys'

    id = db.Column(db.Integer, primary_key=True)
    val = db.Column(db.Text, nullable=False)
    owner_email = db.Column(db.String, db.ForeignKey('users.email'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, val, owner_email):
        self.val = val
        self.owner_email = owner_email

    def __str__(self):
        return self.val

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_owner(owner_email):
        return PubKeyModel.query.filter_by(owner_email=owner_email).first()








