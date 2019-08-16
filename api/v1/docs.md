Schedule
============
    Schedule endpoint serves 2 purposes
        * Book Slot
        * Retrieve Slots for Candidates or Interiewers
    
### Book Slot
##### /api/v1/schedule 
  Books a slot for a particular user identified by the token

* method: POST
* Headers:
* Authorization: Token <token_from_drf_for_the_user> [Required]
* Body:
    + Json:
        
            {
                "start": <epoch_time_stamp> [required]
            }
* Response:
    + Success:
        + status: 200
        + Body:
            +       {"status":"success"}
            

### Retrieve Schedule
##### /api/v1/schedule 
  This api helps in retieving slot information based on parameters. The parameters
  may include 3 combinations
  1. Candidate only
  2. Candidate and Interviewer[s]
  3. Interviewer[s] only

* method: GET
* Headers:
* Authorization: Token <token_from_drf_for_the_user> [Required]
* Params:
    + candidate: [the email id of the candidate]
    + interviewer: [the email id of the interviewer, you can give multiple ]
    
    
        ex: /api/v1/schedule?candidate=1@1.com&interviewer=2@2.com&interviewer3@3.com

* Response:
    + Success:
        + status: 200
        + Body Sample Response:
```
{
   "status":"success",
   "data":[
      {
         "candidate":{
            "name":"someone1",
            "email":"someone1@someone1.com",
            "start":1565968720,
            "end":1565972320
         },
         "interviewers":[
            {
               "email":"interviewer@interviewer.com",
               "name":"interviewer"
            },
            {
               "email":"int2@int2.com",
               "name":"int2"
            }
         ]
      },
      {
         "candidate":{
            "name":"someone2",
            "email":"someone2@someone2.com",
            "start":1565968720,
            "end":1565972320
         },
         "interviewers":[
            {
               "email":"int1@int1.com",
               "name":"int1"
            }
         ]
      }
   ]
}
```
