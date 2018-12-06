import unittest
from flask import json
from app import create_app
from ..api import v1

app = create_app()
database = v1.models.Database()


class TestUsers(unittest.TestCase):

    def setUp(self):
        database.drop_tables()
        database.create_tables()
        app.testing = True
        self.app = app.test_client()
        self.user1 = {
            "firstname": "John",
            "lastname": "Doe",
            "othername": "Jhonny",
            "email": "Doe@demo.com",
            "phoneNumber": "07071010",
            "username": "abc",
            "password": "123",
            "isAdmin": "False"
        }
        self.incident1 = {
            "id": 100,
            "type": "Redflag",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Corruption"
        }
        
    def test_user_signup(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 201)
    
    def test_user_login(self):
        self.app.post('/api/v1/auth/signup', 
                      data=json.dumps(self.user1), 
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/login', 
                                 data=json.dumps(self.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
    
    def test_get_interventions(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.get('/api/v1/interventions')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
    
    def test_get_specific_intervention(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.get('/api/v1/intervention/100')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['data'][0], 100)
    
    def test_delete_record(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.delete('/api/v1/intervention/100')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)

    database.drop_tables()

