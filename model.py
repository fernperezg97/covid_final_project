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

    covidrecords = db.relationship("CovidRecord", back_populates="country")

    def __repr__(self):
        "Show info about country."

        return f"<Country country_id={self.country_id} country={self.country}>"


class CovidRecord(db.Model):
    __tablename__ = 'covidrecords'

    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    country_id = db.Column(db.Integer, db.ForeignKey(Country.country_id))
    date = db.Column(db.Date)
    total_cases = db.Column(db.Integer)

    country = db.relationship("Country", back_populates="covidrecords")

    def __repr__(self):
        "Show info about covidrecord."

        return f"<CovidRecord record_id={self.record_id} country_id={self.country_id}>"

if __name__ == "__main__":
    from server import app

    connect_to_db(app)