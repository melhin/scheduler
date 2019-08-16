# scheduler

A bare minimum interviewer scheduler REST backend.

### What does this have?
Scheduler has an sqlite backed rest backend for demonstration purposes.
There is one endpoint that is public with 2 methods and forms bulk of 
its capablities.

A lot of work can be done via the django admin so that we don't have to 
rebuild the wheel

### How to make it work ?

1. Clone the project 
2. Run the migrations
3. For ease of use a set of users and user profiles are given as fixtures
   load them using `loaddata`
4. For information about api. The endpoint docs are given in the `api/v1/docs.md`
5. To access the api you will need authentication token , to generate it use
   `python manage.py drf_create_token <username>` [to get user name use the django
    admin. ]
6. Admin: username: admin password: admin

