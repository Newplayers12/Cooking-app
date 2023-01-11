# Django-cooking-app
This web app has been developed using the popular Django framework and HTML, CSS and JS for the frontend. Our motivation to build this project is so that we can learn about Django and tighten up our skills. This mini-app can be easily integrated into a bigger system project that needs fundamental features.

### Basic Features of The App
    
* Register – Users can register and create a new profile.
* Login - Registered users can login using username and password.
* User Profile - Once logged in, users can create and update additional information such as avatar and bio in the profile page.
* Modify Profile – Users can update their information such as phone number, birthday, password, avatar and bio.
* Forgot Password – Users can easily retrieve their password if they forget it through email.
* Two Factor Authentication – Users can receive verification code in email inbox to verify account.
* Upload Recipe Posts – Users can upload new recipe post with title, description, ingredients, instructions,...
* View Post Details – Users can read personal posts and others' posts.
* Search Posts – Users can filter by country, date.
* Posts Interaction – Users can interact with recipe posts like save, comment, like.
* Users Interaction – Users can follow each other to see their new posts updated. 
* Admin Panel – Admin can manage users and recipe posts.


### Quick Start
To get this project up and running locally on your computer follow the following steps.
1. Set up a python virtual environment
2. Run the following commands
```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```
   
3. Open a browser and go to http://localhost:8000/