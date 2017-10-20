from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from models import Result

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/kbdbf"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://qgozpitqwkiztq:4744629bc48ab4d7a552d2f355f609cbd28292b56764284676e0ba5e56a7969d@ec2-54-225-88-199.compute-1.amazonaws.com:5432/d7c2rtk4faellk"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db.create_all()
# db.session.commit()

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()