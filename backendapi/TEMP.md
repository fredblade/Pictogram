## Installation pour Mac/Linux

Requis:
python, virtualenv

_NOTE: Selon la version et la façon que Python est installé, il faut utiliser python/pip ou python3/pip3 pour les commandes._

### Créer un environnement virtuel:

### Version 1:

```virtualenv env```

**Activer l'environnement:**

```. env/bin/activate```


### Version 2:

```python3 -m venv env```

**Activer l'environnement:**

```.env/bin/activate```

alternative:

```
cd env
cd bin | cd Scripts
./activate
```

### Installer les modules:

```pip3 install -r requirements.txt```


### Démarrer le serveur:

```python3 manage.py runserver```

# medium

https://medium.com/django-rest/django-rest-framework-b3028b3f0b9

https://blog.logrocket.com/django-rest-framework-build-an-api-in-15-minutes/

```
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py makemigrations
virtualenv env
venv/bin/activate`
```


| ENDPOINT                    | METHOD  | ACTION               |
|-----------------------------|---------|----------------------|
| products/                   | GET     | list()               |
| products/:pk                | GET     | retrieve()           |
| products/get_list           | GET     | get_list()           |
| products/get_product/:pk    | GET     | get_product()        |
| products/delete_product/:pk | DELETE  | delete_product()     |
| products/delete_product/:pk | POST    | delete_product()     |


/profile

voir posts, edit

coucou
coucou123

jakepaul
jakepaul123

select posts_commentitem.id, posts_commentitem.title, posts_commentitem.created, posts_commentitem.post_id_id, posts_commentitem.user_id_id, auth_user.username
from posts_commentitem
left JOIN auth_user
on posts_commentitem.user_id_id = auth_user.id
where posts_commentitem.post_id_id = 24
