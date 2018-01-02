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

class Coin(db.Model):
    __abstract__ = True

    id     = db.Column(db.Integer, primary_key=True)
    date   = db.Column(db.Date,    unique=True)
    open   = db.Column(db.Float,   unique=False, nullable=True)
    high   = db.Column(db.Float,   unique=False, nullable=True)
    low    = db.Column(db.Float,   unique=False, nullable=True)
    close  = db.Column(db.Float,   unique=False, nullable=True)
    volume = db.Column(db.Float,   unique=False, nullable=True)
    marketcap = db.Column(db.Float,unique=False, nullable=True)

    def __init__(self,date,open,high,low,close,volume,marketcap):
        self.date    = date
        self.open    = open
        self.high    = high
        self.low     = low
        self.close   = close
        self.volume  = volume
        self.marketcap = marketcap

    def __repr__(self):
        return '<Date: %s, Open: %s, High: %s, Low: %s, Close: %s, Volume: %s, MarketCap: %s>' \
               % (self.date, self.open, self.high, self.low, self.close, self.volume, self.marketcap)

class Burst(Coin):
    __tablename__ = 'burst'
    __mapper_args__ = {
        'polymorphic_identity': 'burst',
    }

class Bitcoin(Coin):
    __tablename__ = 'bitcoin'
    __mapper_args__ = {
        'polymorphic_identity': 'bitcoin',
    }

class Litecoin(Coin):
    __tablename__ = 'litecoin'
    __mapper_args__ = {
        'polymorphic_identity': 'litecoin',
    }

class Nexus(Coin):
    __tablename__ = 'nexus'
    __mapper_args__ = {
        'polymorphic_identity': 'nexus',
    }