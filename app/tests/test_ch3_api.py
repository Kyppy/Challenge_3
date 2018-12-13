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
        """User info for testing user-related resources"""
        """Valid signup credentials"""
        self.user1 = {
            "firstname": "John",
            "lastname": "Doe",
            "othername": "",
            "email": "Doe@demo.com",
            "phoneNumber": "079-364-0944",
            "username": "B@t5!",
            "password": "Hi_d?.",
            "isAdmin": "False"
        }
        """Bad credentials:Password and username missing"""
        self.user2 = {
            "firstname": "John",
            "lastname": "Doe",
            "othername": "Jhonny",
            "email": "Doe@demo.com",
            "phoneNumber": "079-364-0944",
            "username": "",
            "password": "",
            "isAdmin": "False"
        }
        """Bad credentials:Firstname and lastname missing"""
        self.user3 = {
            "firstname": "",
            "lastname": "",
            "othername": "Jhonny",
            "email": "Doe@demo.com",
            "phoneNumber": "079-364-0944",
            "username": "abc",
            "password": "123",
            "isAdmin": "False"
        }
        """Bad credentials:Poor firstname formatting"""
        self.user4 = {
            "firstname": "J@hn!",
            "lastname": "Doe",
            "othername": "",
            "email": "Doe@demo.com",
            "phoneNumber": "079-364-0944",
            "username": "B@t5!",
            "password": "Hi_d?.",
            "isAdmin": "False"
        }
        """Bad credentials:Poor email formatting"""
        self.user5 = {
            "firstname": "John",
            "lastname": "Doe",
            "othername": "",
            "email": "Doedemo.com",
            "phoneNumber": "079-364-0944",
            "username": "B@t5!",
            "password": "Hi_d?.",
            "isAdmin": "False"
        }
        """Incident records for testing incident-related resources"""
        """Valid 'Intervention' record"""
        self.incident1 = {
            "type": "Intervention",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Corruption"
        }
        """Invalid incident record.Incorrect incident 'type'."""
        self.incident3 = {
            "type": "red-flag",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Corruption"
        }
        """Invalid 'intervention' record.Incident 'comment' missing."""
        self.incident4 = {
            "type": "Intervention",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": ""
        }
        """Valid 'redflag' record."""
        self.red_incident1 = {
            "type": "Redflag",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Violent official."
        }
        """Invalid 'redflag' record.Incorrect incident 'type'"""
        self.red_incident2 = {
            "type": "Intervention",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Violent official."
        }
        """Invalid 'redflag' record.Missing incident 'comment'"""
        self.red_incident3 = {
            "type": "Redflag",
            "location": "100N,50S",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": ""
        }
        
        """Location/comment field for patching."""
        self.patch1 = {
            "location": "[Patched Location]",
            "comment": "[Patched comment]"
        }
        """Invalid Location for patching."""
        self.patch2 = {
            "location": "",
            "comment": "[Patched comment]"
        }
        """Valid comment field for patching."""
        self.patch3 = {
            "location": "[Patched Location]",
            "comment": ""
        }
        """Invalid 'intervention' status patch.No admin privilege"""
        self.int_status1 = {
            "id": 100,
            "isAdmin": False,
            "type": 'Intervention',
            "status": 'Resolved'
        }
        """Invalid 'intervention' status patch.Type is 'Redflag'"""
        self.int_status2 = {
            "id": 100,
            "isAdmin": True,
            "type": 'Redflag',
            "status": 'Resolved'
        }
        """Invalid 'intervention' status patch.Status is invalid"""
        self.int_status3 = {
            "id": 100,
            "isAdmin": True,
            "type": 'Intervention',
            "status": 'Solved'
        }
        """Invalid 'Redflag' status patch.No admin privilege"""
        self.red_status1 = {
            "id": 100,
            "isAdmin": False,
            "type": 'Redflag',
            "status": 'Resolved'
        }
        """Invalid 'Redflag' status patch.Type is 'Intervention'"""
        self.red_status2 = {
            "id": 100,
            "isAdmin": True,
            "type": 'Intervention',
            "status": 'Resolved'
        }
        """Invalid 'Redflag' status patch.Status is invalid"""
        self.red_status3 = {
            "id": 100,
            "isAdmin": True,
            "type": 'Redflag',
            "status": 'Solved'
        }

    """'Signup' resource tests"""
    def test_user_signup(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 201)
    
    def test_user_signup_repeated_credentials(self):
        self.app.post('/api/v1/auth/signup', 
                      data=json.dumps(self.user1), 
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_missing_username_and_password(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user2), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_missing_firstname_and_lastname(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user3), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_bad_firstname_format(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user4), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_user_signup_bad_email_format(self):
        response = self.app.post('/api/v1/auth/signup', 
                                 data=json.dumps(self.user5), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)

    """'Login' Resource tests"""
    def test_valid_user_login(self):
        self.app.post('/api/v1/auth/signup', 
                      data=json.dumps(self.user1), 
                      content_type='application/json')
        response = self.app.post('/api/v1/auth/login', 
                                 data=json.dumps(self.user1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
    
    def test_user_login_missing_username_password(self):
        response = self.app.post('/api/v1/auth/login',
                                 data=json.dumps(self.user2),
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Missing login parameters."
                         "Please check your username "
                         "or password and try again.")

    """ 'GET all interventions' resource test"""
    def test_get_interventions(self):
        self.app.post('/api/v1/interventions',
                      data=json.dumps(self.incident1),
                      content_type='application/json')
        response = self.app.get('/api/v1/interventions')
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)

    """ 'GET specific intervention' resource test"""
    def test_get_specific_intervention(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.get('/api/v1/intervention/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data'][0]["id"], '1')

    def test_get_specific_intervention_missing_id(self):
        response = self.app.get('/api/v1/intervention/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    """ 'GET specific redflag' resource test"""
    def test_get_specific_redflag(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.get('/api/v1/redflag/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['data'][0]["id"], '1')

    def test_get_specific_redflag_missing_id(self):
        response = self.app.get('/api/v1/redflag/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)

    """ POST 'intervention' resource tests"""
    def test_post_invalid_record_type(self):
        response = self.app.post('/api/v1/interventions', 
                                 data=json.dumps(self.incident3), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Incident is not "
                         "type 'Intervention'.")
    
    def test_post_valid_record(self):
        response = self.app.post('/api/v1/interventions', 
                                 data=json.dumps(self.incident1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_record_comment(self):
        response = self.app.post('/api/v1/interventions', 
                                 data=json.dumps(self.incident4), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Intervention has "
                                            "missing 'comment' field.")
    
    """'POST redflag' resource tests"""
    def test_post_valid_record_type(self):
        response = self.app.post('/api/v1/redflags', 
                                 data=json.dumps(self.red_incident1), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
    
    def test_post_invalid_redflag_type(self):
        response = self.app.post('/api/v1/redflags', 
                                 data=json.dumps(self.red_incident2), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Incident is not "
                         "type 'Redflag'.")
    
    def test_post_invalid_record_comment(self):
        response = self.app.post('/api/v1/redflags', 
                                 data=json.dumps(self.red_incident3), 
                                 content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result["message"], "Redflag has "
                                            "missing 'comment' field.")
   
    """'PATCH 'location' and 'comment' tests"""
    def test_patch_intervention_record_with_valid_location(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/interventions/1/location',
                                  data=json.dumps(self.patch1), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_intervention_record_with_invalid_location(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/interventions/1/location',
                                  data=json.dumps(self.patch2), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_intervention_record_with_invalid_comment(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/interventions/1/comment',
                                  data=json.dumps(self.patch3), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_intervention_record_with_valid_comment(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/interventions/1/comment',
                                  data=json.dumps(self.patch1), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_redflags_record_with_valid_location(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/redflags/1/location',
                                  data=json.dumps(self.patch1), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_redflags_record_with_invalid_location(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/redflags/1/location',
                                  data=json.dumps(self.patch2), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_patch_redflags_record_with_valid_comment(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/redflags/1/comment',
                                  data=json.dumps(self.patch1), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_patch_redflags_record_with_invalid_comment(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.patch('/api/v1/redflags/1/comment',
                                  data=json.dumps(self.patch3), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    """ 'Intervention status' test"""
    def test_int_patch_status_no_admin(self):
        response = self.app.patch('/api/v1/interventions/100/status',
                                  data=json.dumps(self.int_status1), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_int_patch_status_bad_type(self):
        response = self.app.patch('/api/v1/interventions/100/status',
                                  data=json.dumps(self.int_status2), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_int_patch_status_bad_status(self):
        response = self.app.patch('/api/v1/interventions/100/status',
                                  data=json.dumps(self.int_status3), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    """ 'Redflag status' test"""
    def test_red_patch_status_no_admin(self):
        response = self.app.patch('/api/v1/redflags/1/status',
                                  data=json.dumps(self.red_status1), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
    
    def test_red_patch_status_bad_type(self):
        response = self.app.patch('/api/v1/redflags/1/status',
                                  data=json.dumps(self.red_status2), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    def test_red_patch_status_bad_status(self):
        response = self.app.patch('/api/v1/redflags/1/status',
                                  data=json.dumps(self.red_status3), 
                                  content_type='application/json')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
    
    """ DELETE 'Intervention' and 'Redflag' tests"""
    def test_delete_intervention_record_with_valid_id(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.delete('/api/v1/intervention/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_intervention_record_with_invalid_id(self):
        self.app.post('/api/v1/interventions', 
                      data=json.dumps(self.incident1), 
                      content_type='application/json')
        response = self.app.delete('/api/v1/intervention/100')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
    
    def test_delete_redflag_record_with_valid_id(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.delete('/api/v1/redflag/1')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_redflag_record_with_invalid_id(self):
        self.app.post('/api/v1/redflags', 
                      data=json.dumps(self.red_incident1), 
                      content_type='application/json')
        response = self.app.delete('/api/v1/redflag/100')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
    
    database.drop_tables()

