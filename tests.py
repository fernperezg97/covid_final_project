class MyWebsiteTests(unittest.TestCase):
    """Testing Flask server"""

    def new_country_shown(self):
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
        self.assertIn(b'')


    def 