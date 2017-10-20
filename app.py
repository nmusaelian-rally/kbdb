from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from models import Result

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/kbdbf"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# db.create_all()
# db.session.commit()

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()