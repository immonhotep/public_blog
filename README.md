# PUBLIC_BLOG

Simple blog application. Backend code developed with python django. Frontend made with free tailwind css elements, and templates.

Website reason : practise Django class based views, and generic class based views.

Application Functions:

Superuser(admin) have extra privileges:
- possiblity to create new categories for posts.
- Read user messages

Regular User :

- list users , followers , followed people
- see other user profile
- follow or unfollow people
- Signup with email confirmation
- login
- update own profile, change email, change password
- create posts by category ( with image upload )
- update own posts
- delete own posts
- like or unlike posts
- send comments, reply comments 
- modify own comments
- delete own comments
- like or unlike comments
- password reset with email confirmation


installation:

1. clone the repository
2. create virtual environment (linux:  virtulenv venv)
3. activate virtual environment  ( source venv/bin/activate )
4. install django with necessary packages ( pip3 install -r requirements.txt )
5. prepare database:  python manage.py makemigrations & python manage.py migrate 
6. create admin user: python manage.py createsuperuser 
7. run the application: python manage.py runserver  
8. login to the application http://127.0.0.1:8000/login/  and create categories, posts etc ..start testing it.

additional information:
- To test working password reset and email confirmation signup: email backend configured currently to localhost port: 1025
- simpliest way to testing on linux to run fake mail server with :
- sudo python3 -m smtpd -n -c DebuggingServer localhost:1025 (deprecated python package, and removed above python 3.12)
- other mail server possiblity to run local 1025 port should also work, or need  modify setting.py  email settings to real mail providers.
