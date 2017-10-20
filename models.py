from app import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'results'

    id  = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(20),   unique=False, nullable=True)
    text = db.Column(db.Text,        unique=False, nullable=True)
    ref  = db.Column(db.String(120), unique=False, nullable=True)

    def __init__(self,tag,text,ref):
        self.tag  = tag
        self.text = text
        self.ref  = ref

    def __repr__(self):
        return '<Result %r>' % self.tag

