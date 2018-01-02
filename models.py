from app import db

class SNP500(db.Model):
    __tablename__ = 'snp500'

    id     = db.Column(db.Integer, primary_key=True)
    date   = db.Column(db.Date,    unique=True)
    sp500  = db.Column(db.Float, unique=False, nullable=True)

    def __init__(self,date,sp500):
        self.date = date
        self.sp500 = sp500

    def __repr__(self):
        return '<%s: %s>' % (self.date, self.sp500)