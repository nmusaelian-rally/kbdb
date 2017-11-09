from app import db
import time
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

class SNP500(db.Model):
    __tablename__ = 'snp500'

    id     = db.Column(db.Integer, primary_key=True)
    date   = db.Column(db.Date,    unique=True)
    sp500  = db.Column(db.Float, unique=False, nullable=True)

    def __init__(self,date,sp500):
        pattern = '%Y-%m-%d'
        #self.date  = int(time.mktime(time.strptime(date, pattern)))
        self.date = date
        self.sp500 = sp500

    def __repr__(self):
        return '<%s: %s>' % (self.date, self.sp500)