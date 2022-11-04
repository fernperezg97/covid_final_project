"""Creating database and tables"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Replace this with your code!


def connect_to_db(flask_app, db_uri="postgresql:///covid", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

class Country(db.Model):
    __tablename__ = 'countries'

    country_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country = db.Column(db.String(50))
    country_slug = db.Column(db.String(50))
    country_code = db.Column(db.String(2))

# class CovidRecord(db.Model):
#     __tablename__ = 'covidrecords'

#     country_id = db.Column(db.Integer, db.ForeignKey(Country.country_id))
#     date = db.Column(db.)

if __name__ == "__main__":
    from server import app

    connect_to_db(app)