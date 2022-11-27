"""CRUD operations"""

from model import db, Country, CovidRecord, User, CurrCountryStat, connect_to_db

if __name__ == '__main__':
    from server import app
    connect_to_db(app)



############## Country Functions ##############



def create_country(name):
    """Create and return a new country."""

    country = Country(country=name)

    return country



def show_all_countries(): 
    """Return all countries"""

    return Country.query.all()



def get_id_by_country_name(name):
    """Get the id of a country by its name."""

    first_country_instance = Country.query.filter_by(country=name).first()

    return first_country_instance.country_id



############## CovidRecord Functions ##############



def create_covid_record(country_id_given, date_given, total_cases_given, total_deaths_given):
    """Create a new covid record instance."""

    covid_record = CovidRecord(country_id=country_id_given, date=date_given, total_cases=total_cases_given, total_deaths=total_deaths_given)

    return covid_record




def get_list_of_days():
    """Grabs all unique days in the database from first recorded day to present."""

    list_of_days = CovidRecord.query.with_entities(CovidRecord.date).distinct().order_by(CovidRecord.date.asc()).all()
    # print(f"\n\n\n\n{list_of_days[0][0]}\n\n\n\n")

    date_list = []
    for day in list_of_days:
        date_list.append(str(day[0]))  
  
    return date_list




def get_country_cases_by_date(user_date):
    """Returns cases for each country by chosen date."""

    country_date_cases = db.session.query(Country.country, CovidRecord.total_cases).join(CovidRecord).filter(CovidRecord.date==user_date).all()
    
    # for instance in country_date_cases:
    #     print(instance)

    return country_date_cases




def get_country_deaths_by_date(user_date):
    """Returns cases for each country by chosen date."""

    country_date_deaths = db.session.query(Country.country, CovidRecord.total_deaths).join(CovidRecord).filter(CovidRecord.date==user_date).all()

    # for instance in country_date_cases:
    #     print(instance)

    return country_date_deaths



    
############## User Functions ##############




def create_user_instance(get_first_name, get_last_name, get_email, get_password):
    """Returns a user instance with an id, first_name, last_name, email, and password."""

    user_instance = User(first_name=get_first_name, last_name=get_last_name, email=get_email, password=get_password)
    db.session.add(user_instance)
    db.session.commit()

    return user_instance



def check_if_user_in_system(check_email, check_password):
    """Checks if a user exists using email, and password provided at login."""

    user_in_system_check = User.query.filter_by(email=check_email, password=check_password).first()   

    return user_in_system_check




    ############## Country Statistics Functions ##############




 
def create_country_stats_instance(country_name_stat, population_stat, total_cases, \
                                 cases_1m_stat, active_cases_stat, total_deaths, \
                                 deaths_1m_stat, total_tests_stat, tests_1m_stat):

    country_stats_record = CurrCountryStat(country_name=country_name_stat, population=population_stat, total_cases_stats=total_cases, \
                                            cases_1m=cases_1m_stat, active_cases=active_cases_stat, total_deaths_stats=total_deaths, \
                                            deaths_1m=deaths_1m_stat, total_tests=total_tests_stat, tests_1m=tests_1m_stat)
    
    return country_stats_record



def stats_per_country(country):
    """Returns all current stats for searched country."""

    country_stats = CurrCountryStat.query.filter_by(country_name=country).first()

    country_stats_dict = country_stats.__dict__
    country_stats_dict.pop('_sa_instance_state', None)

    return country_stats_dict





############## Line Chart Functions ##############





def cases_and_deaths_for_chosen_country(country_provided):
    """Queries the database for all existing records of cases and deaths in order to update the line chart."""

    country_line_graph_stats = db.session.query(Country.country, CovidRecord.date, CovidRecord.total_cases, CovidRecord.total_deaths).join(CovidRecord).filter(Country.country==country_provided).all()
    
    # country_line_graph_stats_dict = country_line_graph_stats.__dict__
    # country_line_graph_stats_dict.pop('_sa_instance_state', None)
    # print(country_line_graph_stats)

    return country_line_graph_stats