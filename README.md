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

### Running Via Docker

1. Install docker-compose up
2. `docker-compose up` this will bring the application up. We are using this
    here because we have to connect to postgress 
3. The migrations and fixture loading are done by default so you dont have to 
4. You should be able to login to the admin http://127.0.0.1:8080/
5. To create tokens to access the api. You should docker exec into the container
    and run the `drf_create_token` to get the token 
    ```
    ./manage.py drf_create_token someone1
    ./manage.py drf_create_token someone2
    ./manage.py drf_create_token someone3
    ./manage.py drf_create_token interviewer
    ./manage.py drf_create_token int1
    ./manage.py drf_create_token int2

    ```

