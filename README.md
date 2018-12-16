# iReporter API  #
[![Build Status](https://travis-ci.org/Kyppy/Challenge_3.svg?branch=develop)](https://travis-ci.org/Kyppy/Challenge_3) [![Coverage Status](https://coveralls.io/repos/github/Kyppy/Challenge_3/badge.svg?branch=develop)](https://coveralls.io/github/Kyppy/Challenge_3?branch=develop) [![Maintainability](https://api.codeclimate.com/v1/badges/51e7d1f45d200f362674/maintainability)](https://codeclimate.com/github/Kyppy/Challenge_3/maintainability)<br>
This project contains resources for the iReporter webapp API. These resources will enable users to signup and login onto the site as well as post,retrieve,update and delete posts. This API uses a postgreSQL database to persist data.

## Motivation ##
<p>Corruption is a serious problem that is rampant throughout Africa.The iReporter web app provides a localised solution that allows any citizen to report any instance of corruption they observe as it occurs and bring it to the attention of authortities as well as the public. It can also be used to report on sitautions that require immediate government intervention.<p>
<p>Users will create and register an account on the iReporter webapp.From their account they can make posts detailing the instance of corruption they encountered. These posts can include images and video. Each post will also contain a geolocation of the event.Users can then track the status of their posts to determine if a particular situation has been resolved, is still under investigation or has been rejected.<p>

## Frameworks Used ##
**Built With:**
* Python 3.7
* PostgreSQL
* Flask 

## Features ##
* Users can create and log onto their iReporter account.
* Users can post incident reports.These reports can be edited or deleted, and can include video,images,latitude-longitude coordinates as well as a comment describing the incident .
* Admin users can determine the validity of a normal user report by marking them as eiether under investigation, resolved or rejected.



## Installation ##
Clone the repository:
```
https://github.com/Kyppy/Challenge_3.git
```

Change into the root directory and create a virtual environment.For example:
```
py -3 -m venv env
```

In the root directory install the dependencies:
```
pip install -r requirements.txt
```

Install PostgreSQL:
```
(Windows) Download and run the PostgreSQL installer: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads#windows
```

Create and initialise the following environment variables:
```
SECRET = <secret string of characters>
DATABASE_URL = dbname=<database name>  user=postgres  password=<database password>
```
## Deployment ##
To run the application change into the root directory and run:
```
run.py
```

To run the unit tests change into the root directory and run the following from the command line:
```
pytest
```

If you want to test the API endpoints yourself, you can use an API development environment such as Postman to access each endpoint URL.Please refer to the API endpoint reference section below:
```
https://www.getpostman.com/apps
```
## API Documentation ##
The documentation below was published using the Postman API development environment.
```
https://documenter.getpostman.com/view/5986402/RzfnhkPU
```
## API Endpoints Reference ##

### Get All Redflag Incident Records ###
Returns a list of dicts containing 'redflag' records.

* URL
   * /api/v1/redflags
   
* Method:
```
   GET
```
* URL Params
   * Required: None 
* Data Params
   * None
* Success Response
   * Code: 200 
```
   Content: {"status":200, "data": <'redflag' records>}
```  
* Error Response
   * If no redflag records exist will return empty list.

### Get All Intervention Incident Records ##
Returns a list of dicts containing 'intervention' records.

* URL
   * /api/v1/interventions

* Method:
```
    GET
```
* URL Params
   * Required: None 
* Data Params
   * None
* Success Response
   * Code: 200 
```
   Content: {"status":200, "data": <'intervention' records>}
```  
* Error Response
   * If no intervention records exist will return empty list.

### Get A Specific Redflag Incident ##
Returns a dict of containing a single 'redflag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflag/<int:red_flag_id>

* Method:
```
    GET
```
* URL Params
   * Required: redflag_id=[integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
```
   Content: {"status":200, "data": <'redflag' record>}
```
* Error Response
   * Code: 404 NOT FOUND<br>
    Content: { "status": 404, "message": "An incident with id <redflag_id> does not exist." }<br>

    OR

   * Code: 400 BAD REQUEST<br>
   Content: {"status": 400, "message": "Invalid incident id in URL"}

### Get A Specific Intervention Incident ##
Returns a dict of a single 'intervention' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflag/<int:intervention_id>

* Method:
```
   GET
```
* URL Params
   * Required: intervention_id = [integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
```
   Content: {"status":200, "data": <'intervention' record>}
```   
* Error Response
   * Code: 404 NOT FOUND<br>
    Content: { "status": 404, "message": "An incident with id <intervention_id> does not exist." }<br>

    OR

   * Code: 400 BAD REQUEST<br>
   Content: {"status": 400, "message": "Invalid incident id in URL"}

### Post A Redflag Incident ##
Stores a dict of a single 'redflag' record on the database. Record is specified by its 'id' field.

* URL
   * /api/v1/redflags

* Method:
```
   POST
```
* URL Params
   * None 
* Data Params
```
Required:{"type":"Redflag"}
Required:{"location":"<lat-long cooridnate>"}
Optional:{"Images":"<img file url>"}
Optional:{"Videos":"<video file url>"}
Required:{"comment":"<comment string>"}

```
* Success Response
   * Code: 201
```
   Content: return {"status":201, "data":{"id":<redflag record id>, "message":"created redflag record"}}
``` 
* Error Response
   * Code: 400 BAD REQUEST<br>
    Content: { "message": "Redflag has missing 'comment' field."}<br>

   OR

   * Code: 400 BAD REQUEST<br>
   Content: { "message": "Incident is not type 'Redflag'." }<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: { "message": "Location field is missing or formatted incorrectly.Please ensure it is formatted as a latitude-longitude coordinate e.g. '15N,45E'." }

### Post An Intervention Incident ##
Stores a dict of a single 'intervention' record on the database. Record is specified by its 'id' field.

* URL
   * /api/v1/interventions

* Method:
```
   POST
```
* URL Params
   * None 
* Data Params
```
Required:{"type":"Intervention"}
Required:{"location":"<lat-long cooridnate>"}
Optional:{"Images":"<img file url>"}
Optional:{"Videos":"<video file url>"}
Required:{"comment":"<comment string>"}

```
* Success Response
   * Code: 201
```
   Content: return {"status":201, "data":{"id": <intervention id>, "message":"created intervention record"}}
```  
* Error Response
   * Code: 400 BAD REQUEST<br>
    Content: { "message": "Intervention has missing 'comment' field."}<br>

   OR

   * Code: 400 BAD REQUEST<br>
   Content: { "message": "Incident is not type 'Intervention'." }<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: { "message": "Location field is missing or formatted incorrectly.Please ensure it is formatted as a latitude-longitude coordinate e.g. '15N,45E'." }

### Update The Location Field Of A Redflag Incident ##
Edits the 'location' field of a single 'redflag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflags/<int:redflag_id>/location

* Method:
```
   PATCH
```
* URL Params
   * Required: redflag_id=[integer] 
* Data Params
```
Required:{"location":"<lat-long cooridnate>"}
```
* Success Response
   * Code: 200
```
   Content: return {"status":200, "data":{"id": <redflag record id>, "message":"Updated redflag record's location"}}
```  
* Error Response
   * Code: 403 NOT AUTHORIZED<br>
    Content: {"message": "Incident id associated with other user account. Please select an incident id for one of your existing posts."}<br>

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Location field is formatted incorrectly. Please ensure it is formatted as a latitude-longitude coordinate e.g '15N,45E'."}<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Bad credentials.Login failed"}<br>

   OR

   * Code: 404 FILE NOT FOUND<br>
   Content: {"message": "No record with id <redflag_id> exists."

### Update The Location Field Of An Intervention Incident ##
Edits the 'location' field of a single 'intervention' record. Record is specified by its 'id' field.

* URL
   * /api/v1/interventions/<int:intervention_id>/location

* Method:
```
   PATCH
```
* URL Params
   * Required: intervention_id=[integer] 
* Data Params
```
Required:{"location":"<lat-long cooridnate>"}
```
* Success Response
   * Code: 200
```
   Content: return {"status":200, "data":{"id": <intervention record id>, "message":"Updated intervention record's location"}}
```  
* Error Response
   * Code: 403 NOT AUTHORIZED<br>
    Content: {"message": "Incident id associated with other user account. Please select an incident id for one of your existing posts."}<br>

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Location field is formatted incorrectly. Please ensure it is formatted as a latitude-longitude coordinate e.g '15N,45E'."}<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Bad credentials.Login failed"}<br>

   OR

   * Code: 404 FILE NOT FOUND<br>
   Content: {"message": "No record with id <intervention_id> exists."

### Edit The Comment Field Of A Redflag Incident ##
Edits the 'comment' field of a single 'redflag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflags/<int:redflag_id>/comment

* Method:
```
   PATCH
```
* URL Params
   * Required: redflag_id =[integer] 
* Data Params
```
Required:{"comment":"<comment string>"}
```
* Success Response
   * Code: 200
```
   Content: return {"status":200, "data":{"id": <redflag record id>, "message":"Updated redflag record's comment"}}
```  
* Error Response
   * Code: 403 NOT AUTHORIZED<br>
    Content: {"message": "Incident id associated with other user account. Please select an incident id for one of your existing posts."}<br>

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Missing update information. Check your input and try again."}<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Bad credentials.Login failed"}<br>

   OR

   * Code: 404 FILE NOT FOUND<br>
   Content: {"message": "No record with id <reflag_id> exists."}

### Edit The Comment Field Of An Intervention Incident ##
Edits the 'comment' field of a single 'intervention' record. Record is specified by its 'id' field.

* URL
   * /api/v1/interventions/<int:intervention_id>/comment

* Method:
```
   PATCH
```
* URL Params
   * Required: intervention_id =[integer] 
* Data Params
```
Required:{"comment":"<comment string>"}
```
* Success Response
   * Code: 200
```
   Content: return {"status":200, "data":{"id": <intervention record id>, "message":"Updated intervention record's comment"}}
```   
* Error Response
   * Code: 403 NOT AUTHORIZED<br>
    Content: {"message": "Incident id associated with other user account. Please select an incident id for one of your existing posts."}<br>

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Missing update information. Check your input and try again."}<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Bad credentials.Login failed"}<br>

   OR

   * Code: 404 FILE NOT FOUND<br>
   Content: {"message": "No record with id <reflag_id> exists."}
  
### Delete A Specific Redflag Incident ##
Removes a single 'redflag' record from the database. Record is specified by its 'id' field.

* URL
   * /api/v1/redflag/<int:redflag_id>

* Method:
```
   DELETE
```
* URL Params
   * Required: redflag_id =[integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
```
   Content: {"status":200, "data":{"id": <redflag record id>, "message": "Redflag record has been deleted."}}
```  
* Error Response
   * Code: 403 NOT AUTHORIZED<br>
    Content: {"message": "Incident id associated with other account. Please select an incident id for one of your existing posts."}<br>  

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "No incident id provided"}<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Invalid incident id in URL"}<br>

   OR

   * Code: 404 FILE NOT FOUND<br>
   Content: {"message": "No record with id <reflag_id> exists."}

### Delete A Specific Intervention Incident ##
Removes a single 'intervention' record from the database. Record is specified by its 'id' field.

* URL
   * /api/v1/intervention/<int:intervention_id>

* Method:
```
   DELETE
```
* URL Params
   * Required: intervention_id=[integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
```
   Content: {"status":200, "data":{"id": <intervention record id>, "message": "Intervention record has been deleted."}}
```   
* Error Response
   * Code: 403 NOT AUTHORIZED<br>
    Content: {"message": "Incident id associated with other account. Please select an incident id for one of your existing posts."}<br>  

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "No incident id provided"}<br>
  
   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Invalid incident id in URL"}<br>

   OR

   * Code: 404 FILE NOT FOUND<br>
   Content: {"message": "No record with id <intervention_id> exists."}

### Create A User Account ##
Creates a new user account and inserts their registration data into a database record. Provides a JWT authorization token upon successful registration. 

* URL
   * /api/v1/auth/signup

* Method:
```
   POST
```
* URL Params
   * None 
* Data Params
```
Required:{"firstname":"<name>"}
Required:{"lastname":"<name>"}
Optional:{"othername":"<name>"}
Required:{"email":"<email address>"}
Required:{"phoneNumber":"<phone number formatted as 111-222-3333>"}
Required:{"username":"<username>"}
Required:{"password":"<password>"}
```
* Success Response
   * Code: 201 
```
   Content: {"status":201, {"token": <JWT auth token>, "user": "Sign-up Complete! Welcome to the app <username>!"}
                         
```   
* Error Response
   * Code: 400 BAD REQUEST<br>
    Content: {"message": "Bad credentials. Signup failed"}<br>  

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Signup failed. Please ensure that your credentials are correctly formatted."} 
  
### Login A User ##
Logs in a registered user into the app. Provides a JWT authorization token upon successful login.

* URL
   * /api/v1/auth/login

* Method:
```
   POST
```
* URL Params
   * None 
* Data Params
```
Required:{"username":"<username>"}
Required:{"password":"<password>"}
```
* Success Response
   * Code: 200 
```
   Content: {"status":200, {"token": <JWT auth token>, "user": "Login successful. Welcome back <username>."}
                    
```   
* Error Response
   * Code: 400 BAD REQUEST<br>
    Content: {"message": "Missing login parameters.Please check your username or password and try again."}<br> 

   OR

   * Code: 400 BAD REQUEST<br>
   Content: {"message": "Bad credentials.Login failed"}

### Owner ###
Kyppy Simani