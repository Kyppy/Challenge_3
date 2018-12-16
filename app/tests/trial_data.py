class TestData():
    def __init__(self):
        """User info for testing user-related resources"""
        """Valid signup credentials"""
        self.user0 = {
            "firstname": "John",
            "lastname": "Doe",
            "othername": "",
            "email": "Brian@demo.com",
            "phoneNumber": "079-364-0944",
            "username": "NSP",
            "password": "Danny69",
            "isAdmin": "False"
        }
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
            "location": "10N,50E",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Corruption"
        }
        """Invalid incident record.Incorrect incident 'type'."""
        self.incident3 = {
            "type": "red-flag",
            "location": "10N,50E",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Corruption"
        }
        """Invalid 'intervention' record.Incident 'comment' missing."""
        self.incident4 = {
            "type": "Intervention",
            "location": "10N,50E",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": ""
        }
        """Valid 'redflag' record."""
        self.red_incident1 = {
            "type": "Redflag",
            "location": "10N,50E",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Violent official."
        }
        """Invalid 'redflag' record.Incorrect incident 'type'"""
        self.red_incident2 = {
            "type": "Intervention",
            "location": "10N,50E",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": "Violent official."
        }
        """Invalid 'redflag' record.Missing incident 'comment'"""
        self.red_incident3 = {
            "type": "Redflag",
            "location": "10N,50E",
            "Images": "[Images]",
            "Videos": "[Videos]",
            "comment": ""
        }
        """Location/comment field for patching."""
        self.patch1 = {
            "location": "90S,12W",
            "comment": "[Patched comment]"
        }
        """Invalid Location for patching."""
        self.patch2 = {
            "location": "150E,400W",
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
