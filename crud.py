"""CRUD operations"""

from model import db, Country, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)



    



def create_country(name, slug, country_code):
    """Create and return a new country."""

    country = Country(country=name, country_slug=slug, country_code=country_code)

    return country

def show_all_countries(): 
    """return all countries"""

    return Country.query.all()


def get_country_by_code(country_code):
    country_by_id = Country.query.get(country_code)

    return country_by_id





