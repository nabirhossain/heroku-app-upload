# How to upload a Django app on heroku 

1st Step(Python heroku venv(initialize Project)) 

1. Create virtual environment: ```python3 -m venv myenv```
2. Activate virtual environment: ```source myenv/bin/activate```
3. Install Django: ```pip install django```
4. Create Django Project: ```django-admin startproject DeployProject```
5. CD to DeployProject folder: ```cd DeployProject```
  (1)  git init  (2) git add .    (3) git commit -m “initial“ 
  
7. Run server: 
```python manage.py runserver```

> 2nd Step 
1. Open ```DeployProject``` folder in text editor
2. Create ```.gitignore ``` file on top level directory
3. Add this 3 lines to ```.gitignore``` file:
```
   __pycache__/
   db.sqlite3
   *.pyc
```
> 3rd Step(Heroku setup)
1. Log in to heroku: 
```
heroku login
```
2. Create a heroku app: 
```
heroku create appname
```
3. Create ```runtime.txt ``` file on top level directory then add: 
```
python-3.6.4
```
4. Install gunicorn: 
```
pip install gunicorn
```
5. Create ```requirements.txt``` file on top level of directory and copy paste pip freeze results into it.

6. Create ```Procfile``` on top level of directory and add this:
```
web: gunicorn DpProject.wsgi --log-file - 
```
7. install ```Whitenoise``` then copy paste to ```requirements.txt``` : 
```
pip install whitenoise
```
8. In ```settings```, add static root vvariable, below static url variable: 
```
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
9. Static file storage settings :
``` 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
```
10.Media file setting:
```
MEDIA_URL = "/media/" 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```   
12. Middleware setting under security middleware :
```
'whitenoise.middleware.WhiteNoiseMiddleware',
```
> 4th Step (Database Configurations & Run app)

1. Install ``` dj database url ```, then copy paste to ```requirements.txt ```: 
```
pip install dj-database-url
```

2. line below: 
```
psycopg2
```

3. At bottom of settings: 
```
import dj_database_url
line below: db_from_env = dj_database_url.config()
line below: DATABASES['default'].update(db_from_env)
```
5.Set your host in settings:  
```
ALLOWED_HOSTS = ['blog18.herokuapp.com']
```
Again command 
```
 (1)git add (2) git commit -m “inital 2”
```
7.Disable or debug Static: 
```
heroku config:set DISABLE_COLLECTSTATIC=1
```
8. Run heroku: 
```
git push heroku master 
```
9. Migrate heroku database: 
```
heroku run python manage.py migrate
```
10.Create superuser on heroku admin for access your app : 
```
heroku run python manage.py createsuperuser
```
12. Run heroku server: 
```
heroku run python manage.py runserver
```
11. Open: 
```
heroku open
```
  > -----------------------------------------------------------------------------------------------------------------------------
Install all pip into one command: 
```
pip install -r requirements.txt
```

Automatically include all pip in ```requirements.txt``` file: 
```
pip freeze > requirements.txt
```
