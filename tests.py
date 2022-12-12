import crud
import unittest
import server
import json

class MyWebsiteTests(unittest.TestCase):
    """Testing Flask server"""

    def test_new_country_is_shown(self):
        """When user types in a country, it should bring you to the '/country-search' route and it should included a country's population."""

        client = server.app.test_client()
        result = client.get('/country-search')

        self.assertIn(b'Population', result.data)
        


    def test_user_registration(self):
        """POST request test."""

        client = server.app.test_client()
        result = client.post('/user-registration-info', data={'first_name': 'Jane',
                                                            'last_name': 'Doe',
                                                            'email': 'janedoe@gmail.com',
                                                            'password': 'password1'})
        self.assertIn(b'Create Your Account')


        
    def test_if_user_created(self):
        """Checks if user added to database after entering all required credentials."""

        user_instance = crud.create_user_instance("test0", "test1", "test2", "test3")
        
        self.assertTrue(user_instance.first_name == "test0")
        self.assertTrue(user_instance.last_name == "test1")
        self.assertTrue(user_instance.email == "test2")
        self.assertTrue(user_instance.password == "test3")

# Michael
    #    result = client.post('/user-registration-check', 
    #                          data=json.dumps(dict(email= 'janedoe@gmail.com',password= 'password1', firstName='Jane', lastName='Doe')),
    #                          content_type="application/json")

    def test_user_validation(self):
        """Check the route that validates a user. Provide a pretend email/password and check the return is a dictionary with an unsuccessful status"""

        client = server.app.test_client()
        result = client.post('/user-registration-check', 
                             data=json.dumps(dict(email= 'test@gmail.com', password= 'test1234', firstName="bad", lastName="guy")),
                             content_type='application/json')

        self.assertEqual(result, {"result": "unsuccessful", "status": "USER ALREADY EXISTS OR CREDENTIALS INVALID."})



    def test_user_taken_to_timeline(self):
        """ Tests that user is taken to COVID timeline page after receiving dictionary response with 'result': 'sucessful' """

        client = server.app.test_client()
        result = client.post('/user-registration-check')

        self.assertTrue(result == {"result": "sucessful", "status": "LOGIN WITH YOUR NEW CREDENTIALS."}) 