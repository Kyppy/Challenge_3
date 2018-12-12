# iReporter Persistent Data API #
This project contains resources for the iReporter webapp API. These resources will enable users to signup and login onto the site as well as post,retrieve,edit and delete posts. This API uses a postgreSQL database to persist data.

### Continuous Integration Badges ###
[![Build Status](https://travis-ci.org/Kyppy/Challenge_3.svg?branch=develop)](https://travis-ci.org/Kyppy/Challenge_3)

[![Coverage Status](https://coveralls.io/repos/github/Kyppy/Challenge_3/badge.svg?branch=develop)](https://coveralls.io/github/Kyppy/Challenge_3?branch=develop)

[![Maintainability](https://api.codeclimate.com/v1/badges/51e7d1f45d200f362674/maintainability)](https://codeclimate.com/github/Kyppy/Challenge_3/maintainability)

## Endpoint Documentation ##

## Get All Redflag Incident Records ##
Returns a list of 'red-flag' records as dicts.

* URL
   * /api/v1/redflags
* Method:
   * GET
* URL Params
   * Required: None 
* Data Params
   * None
* Success Response
   * Code: 200 
   * Content: {"status":200, "data":[list of dicts]}
   
* Error Response
   * If no redflag records exist will return empty list.

## Get All Intervention Incident Records ##
Returns a list of 'red-flag' records as dicts.

* URL
   * /api/v1/interventions
* Method:
   * GET
* URL Params
   * Required: None 
* Data Params
   * None
* Success Response
   * Code: 200 
   * Content: {"status":200, "data":[list of dicts]}
   
* Error Response
   * If no intervention records exist will return empty list.

## Get A Specific Redflag Incident ##
Returns a dict of a single 'red-flag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflag/<int:red_flag_id>
* Method:
   * GET
* URL Params
   * Required: red_flag_id = [integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
   * Content: {"status":200, "data":[redflag record]}
   
* Error Response
   * Code: 404
   * Content: {"status":404, "message":"An incident with id '<red_flag_id>' does not exist."}

## Get A Specific Intervention Incident ##
Returns a dict of a single 'intervention' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflag/<int:intervention_id>
* Method:
   * GET
* URL Params
   * Required: intervention_id = [integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
   * Content: {"status":200, "data":[intervention record]}
   
* Error Response
   * Code: 404
   * Content: {"status":404, "message":"An incident with id '<intervention_id>' does not exist."}

## Post A Redflag Incident ##
Posts a dict of a single 'redflag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/redflags
* Method:
   * POST
* URL Params
   * None 
* Data Params
   * None
* Success Response
   * Code: 201
   * Content: return {"status":201, "data":{"id":<red_flag_id>, "message":"created redflag record"}}
   
* Error Response
   * Code: 400
   * Content:<p> {"message":"A red-flag with id '<red_flag_id>' already exists."}<br> 
                  OR<br>
                 {"message":"'id '<red_flag_id>' of request body and 'id' '<url_input>' of url do not match"<p>
 
## Edit The Location Field Of A Redflag Incident ##
Edits the 'location' field of a single 'red-flag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/red_flag/<int:red_flag_id>/location
* Method:
   * PATCH
* URL Params
   * Required: red_flag_id =[integer] 
* Data Params
   * None
* Success Response
   * Code: 200
   * Content: return {"status":200, "data":{"id":'<red_flag_id>', "message":"Updated red-flag record's location"}}
   
* Error Response
   * Code: 400,404
   * Content:<p> {"message":"A red-flag with id '<red_flag_id>' already exists."}<br> 
                  OR<br>
                 {"message":"'id '<red_flag_id>' of request body and 'id' '<url_input>' of url do not match"<br>
                  OR<br>
                 {"message":"Location update data was not provided."}<p>

## Edit The Comment Field Of A Redflag Incident ##
Edits the 'comment' field of a single 'red-flag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/red_flag/<int:red_flag_id>/comment
* Method:
   * PATCH
* URL Params
   * Required: red_flag_id =[integer] 
* Data Params
   * None
* Success Response
   * Code: 200
   * Content: return {"status":200, "data":{"id":'<red_flag_id>', "message":"Updated red-flag record's comment"}}
   
* Error Response
   * Code: 400,404
   * Content:<p> {"message":"A red-flag with id '<red_flag_id>' already exists."}<br> 
                  OR<br>
                 {"message":"'id '<red_flag_id>' of request body and 'id' '<url_input>' of url do not match"<br>
                  OR<br>
                 {"message":"Comment update data was not provided."}<p>
  
## Delete A Specific 'red-flag' Incident ##
Removes the dict of a single 'red-flag' record. Record is specified by its 'id' field.

* URL
   * /api/v1/red_flag/<int:red_flag_id>
* Method:
   * DELETE
* URL Params
   * Required: red_flag_id =[integer] 
* Data Params
   * None
* Success Response
   * Code: 200 
   * Content: {"status":200, "data":{"id":'<red_flag_id>', "message":"red-flag record has been deleted"}}
   
* Error Response
   * Code: 404
   * Content: {"status":404, "message":"An incident with id '<red_flag_id>' does not exist."}