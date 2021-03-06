# scheduler

A bare minimum interviewer scheduler REST backend.

### What does this have?
Scheduler has postgres based rest backend for demonstration purposes.
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

### How to create users ?

For now there are no api for registering or login. Everything can be done via the admin
Admin can be used heavily for administation purposes and easy access to slots

1. Login to the admin
2. Go to the User model and create a user
3. You must also create a user profile [this marks the user as candidate or interview]
    We have it as a seperate model for extension purposes
4. Create tokens from Django Admin Auth Tokens
5. Slots can be seen in the Slot model

### Running Via Docker

1. Install docker-compose up
2. `docker-compose up` this will bring the application up. We are using this
    here because we have to connect to postgress 
3. The migrations and fixture loading are done by default so you dont have to 
4. You should be able to login to the admin http://127.0.0.1:8080/
