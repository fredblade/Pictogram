# Pictogram: Social Media API

I created this app to learn about Django and its REST framework. My time limit was 5 weeks. This API was used with a React Native frontend (Android and Web). Feel free to improve/use this.


### Features:

- Register/Login with JWT token (if desired, change the token lifespan in medium/settings.py)
- Image upload (Either in png/jpg or Base64 string for Android)

### Actions:

- Create, read, edit, delete posts, profile picture
- Create, read, delete comments

### Run the API

```cd backendapi```

```python3 manage.py runserver```

### Usage

The file DJANGO_APP.postman_collection.json contains the core requests to use the API. You can find all the gateways by looking in all the urls.py files.

### Install modules
```pip3 install -r requirements.txt```
python3 manage.py runserver 0.0.0.0:8000

### Want to change the data models?
python3 manage.py makemigrations
python3 manage.py migrate

### Creation an admin user
python3 manage.py createsuperuser

Access the admin panel at localhost:8000/admin
