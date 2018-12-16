import unittest
from flask import json
from app import create_app
from ..api import v1
from .trial_data import TestData
app = create_app()
udb = v1.users.users_models.UsersDatabase()
idb = v1.incidents.incident_models.IncidentsDatabase()
td = TestData()


class TestRedflags(unittest.TestCase):

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
        
    """ 'GET specific redflag' resource test"""
    def test_get_specific_redflag(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.get('/api/v1/redflag/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data'][0]["id"], 1)
    
    def test_get_specific_redflag_missing_id(self):
        response = self.app.get('/api/v1/redflag/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    """'POST redflag' resource tests"""
    def test_post_valid_record_type(self):
        response = self.app.post('/api/v1/redflags', 
                                 data=json.dumps(td.red_incident1), 
                                 content_type='application/json',
                                 headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_redflag_type(self):
        response = self.app.post('/api/v1/redflags', 
                                 data=json.dumps(td.red_incident2), 
                                 content_type='application/json',
                                 headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Incident is not "
                         "type 'Redflag'.")
    
    def test_post_invalid_record_comment(self):
        response = self.app.post('/api/v1/redflags', 
                                 data=json.dumps(td.red_incident3), 
                                 content_type='application/json',
                                 headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Redflag has "
                                            "missing 'comment' field.")
    
    """'PATCH 'location' and 'comment' tests"""
    def test_patch_redflags_record_with_valid_location(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/redflags/1/location',
                                  data=json.dumps(td.patch1), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_redflags_record_with_invalid_location(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/redflags/1/location',
                                  data=json.dumps(td.patch2), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_redflags_record_with_valid_comment(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/redflags/1/comment',
                                  data=json.dumps(td.patch1), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_redflags_record_with_invalid_comment(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.patch('/api/v1/redflags/1/comment',
                                  data=json.dumps(td.patch3), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    """ 'Redflag status' test"""
    def test_red_patch_status_no_admin(self):
        response = self.app.patch('/api/v1/redflags/1/status',
                                  data=json.dumps(td.red_status1), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_red_patch_status_bad_type(self):
        response = self.app.patch('/api/v1/redflags/1/status',
                                  data=json.dumps(td.red_status2), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_red_patch_status_bad_status(self):
        response = self.app.patch('/api/v1/redflags/1/status',
                                  data=json.dumps(td.red_status3), 
                                  content_type='application/json',
                                  headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    """ DELETE 'Intervention' and 'Redflag' tests"""
    def test_delete_redflag_record_with_valid_id(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.delete('/api/v1/redflag/1', 
                                   headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_redflag_record_with_invalid_id(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(td.red_incident1), 
                      content_type='application/json',
                      headers={"Authorization": self.access})
        response = self.app.delete('/api/v1/redflag/100', 
                                   headers={"Authorization": self.access})
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
    
udb.drop_tables()
idb.drop_tables()