import unittest
from flask import json
from app import create_app
from ..api import v1
from .trial_data import TestData
app = create_app()
udb = v1.users.users_models.UsersDatabase()
idb = v1.incidents.incident_models.IncidentsDatabase()
td = TestData()


class TestUsers(unittest.TestCase):

    def setUp(self):
        udb.drop_tables()
        idb.drop_tables()
        udb.create_tables()
        idb.create_tables()
        app.testing = True
        self.app = app.test_client()

    """'Signup' resource tests"""
    def test_user_signup(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)

    def test_user_signup_repeated_credentials(self):
        self.app.post('/api/v1/auth/signup', 
                      data=json.dumps(td.user1), 
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        
    def test_user_signup_missing_username_and_password(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user2), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_missing_firstname_and_lastname(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user3), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_bad_firstname_format(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user4), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_bad_email_format(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user5), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    """'Login' Resource tests"""
    def test_valid_user_login(self):
        self.app.post('/api/v1/auth/signup', 
                      data=json.dumps(td.user1), 
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/login', 
                                 data=json.dumps(td.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
    
    def test_user_login_missing_username_password(self):
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(td.user2),
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Missing login parameters."
                         "Please check your username "
                         "or password and try again.")

udb.drop_tables()
idb.drop_tables()