import unittest
from flask import json
from app import create_app

app = create_app()

class TestUsers(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
    
    def test_user_signup(self):
        response = self.app.post('/api/v1/auth/signup')
        result = json.loads(response.data)
        self.assertEqual(result['status'],200)

    def test_user_login(self):
        response = self.app.post('/api/v1/auth/login')
        result = json.loads(response.data)
        self.assertEqual(result['status'],200)
    
    def test_get_interventions(self):
        response = self.app.get('/api/v1/interventions')
        result = json.loads(response.data)
        self.assertEqual(result['status'],200)
        self.assertEqual(result['data'],intervention_data)
    
    def test_get_specific_intervention(self):
        response = self.app.get('/api/v1/interventions/<intervention_id>')
        result = json.loads(response.data)
        self.assertEqual(result['status'],200)
        self.assertEqual(result['data'],intervention_data)
    
    def test_admin_edit_redflag_status(self):
        response = self.app.patch('/api/v1/red_flags/800/status', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(red_flag['status'],data['status'])

    def test_admin_edit_intervention_status(self):
        response = self.app.patch('/api/v1/interventions/800/status', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(intervention['status'],data['status'])
    
    def test_admin_edit_intervention_comment(self):
        response = self.app.patch('/api/v1/interventions/800/comment', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(intervention['comment'],data['comment'])
    
    def test_admin_edit_intervention_location(self):
        response = self.app.patch('/api/v1/interventions/800/location', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(intervention['location'],data['location'])
    
    def test_delete_record(self):
        self.app.post('/api/v1/intervention/800', data=json.dumps(self.data), content_type='application/json')
        response = self.app.delete('/api/v1/red_flag/800')
        result = json.loads(response.data)
        self.assertEqual(result['status'],200)
        self.assertEqual(intervention,None)

    def test_post_incident_record(self):
        response = self.app.post('/api/v1/interventions', data=json.dumps(self.data), content_type='application/json')
        self.assertEqual(response.status_code,201)
        self.assertEqual(new_intervention['data'],data['data'])
        
    
"""
Arbitrary change to test Coveralls.Change
"""
    
      

