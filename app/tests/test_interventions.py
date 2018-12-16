import unittest
from flask import json
from app import create_app
from ..api import v1
from .trial_data import TestData
app = create_app()
udb = v1.users.users_models.UsersDatabase()
idb = v1.incidents.incident_models.IncidentsDatabase()
td = TestData()


class TestInterventions(unittest.TestCase):

    def setUp(self):
        udb.drop_tables()
        idb.drop_tables()
        udb.create_tables()
        idb.create_tables()
        app.testing = True
        self.app = app.test_client()

        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(td.user0), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 201)
        self.token = result['data'][0]['token']
        self.access = "Bearer {}".format(self.token)
      
    """ 'GET all interventions' resource test"""
    def test_get_interventions(self):
        self.app.post('/api/v1/interventions',
                      data=json.dumps(td.incident1),
                      content_type='application/json')
        response = self.app.get('/api/v1/interventions')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)

    """ 'GET specific intervention' resource test"""
    def test_get_specific_intervention(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.get('/api/v1/intervention/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data'][0]["id"], 1)
    
    def test_get_specific_intervention_missing_id(self):
        response = self.app.get('/api/v1/intervention/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
    
    """ POST 'intervention' resource tests"""
    def test_post_invalid_record_type(self):
        response = self.app.post('/api/v1/interventions', 
                                 data=json.dumps(td.incident3), 
                                 content_type='application/json',
                                 headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Incident is not "
                         "type 'Intervention'.")
    
    def test_post_valid_record(self):
        response = self.app.post('/api/v1/interventions', 
                                 data=json.dumps(td.incident1), 
                                 content_type='application/json',
                                 headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_record_comment(self):
        response = self.app.post('/api/v1/interventions', 
                                 data=json.dumps(td.incident4), 
                                 content_type='application/json',
                                 headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Intervention has "
                                            "missing 'comment' field.")
    
    """'PATCH 'location' and 'comment' tests"""
    def test_patch_intervention_record_with_valid_location(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/interventions/1/location',
                                  data=json.dumps(td.patch1), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_intervention_record_with_invalid_location(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/interventions/1/location',
                                  data=json.dumps(td.patch2), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_intervention_record_with_invalid_comment(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/interventions/1/comment',
                                  data=json.dumps(td.patch3), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_intervention_record_with_valid_comment(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/interventions/1/comment',
                                  data=json.dumps(td.patch1), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    """ 'Intervention status' test"""
    def test_int_patch_status_no_admin(self):
        response = self.app.patch('/api/v1/interventions/100/status',
                                  data=json.dumps(td.int_status1), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_int_patch_status_bad_type(self):
        response = self.app.patch('/api/v1/interventions/100/status',
                                  data=json.dumps(td.int_status2), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_int_patch_status_bad_status(self):
        response = self.app.patch('/api/v1/interventions/100/status',
                                  data=json.dumps(td.int_status3), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    """ DELETE 'Intervention' and 'Redflag' tests"""
    def test_delete_intervention_record_with_valid_id(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.delete('/api/v1/intervention/1', 
                                   headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_intervention_record_with_invalid_id(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(td.incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.delete('/api/v1/intervention/100', 
                                   headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
    
udb.drop_tables()
idb.drop_tables()