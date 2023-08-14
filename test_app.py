import unittest
from app import app

class FlaskAppTests(unittest.TestCase):
    
    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        self.app.testing = True 
    
    def test_home_status_code(self):
        # Sends an HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # Assert that the HTTP status code is 200 (OK)
        self.assertEqual(result.status_code, 200)

    def test_home_data(self):
        # Sends an HTTP GET request to the application
        # on the specified path
        result = self.app.get('/') 

        # Assert that the response data matches
        self.assertEqual(result.data, b'this is coming from v1')

if __name__ == "__main__":
    unittest.main()