# Approach

The application has been developed using Python 3.6.8, Django as its back-end with the Django REST Framework and Vue JS as the front-end. PostgreSQL has been used as the database. After completion, the application has been deployed at Heroku. Please check out the live version of the application: [favoritethingsmutasim.herokuapp.com](https://favoritethingsmutasim.herokuapp.com/)

# Deployment Methods

To start the development of the application, the following commands were performed in sequence:

```bash
virtualenv venv -p python3
cd venv
pip install django djangorestframework dj-database-url django-braces gunicorn psycopg2-binary python-decouple whitenoise
django-admin startproject src
```

Once the installation of the packages were finished, the application was made live in the local environment with the following commands:

```bash
cd src
python manage.py migrate
python manage.py runserver
```

As the development some variables in the `settings.py` were made private, i.e., `SECRET_KEY`, etc. These variables were defined in a `.env` file at the root of the project and included in the `.gitignore` file. The `python-decouple` package was utilized to access the values of these variables. For deployment, the project settings in the Heroku dashboard allows enabling ennvironment variables, which were utilized for these sensitive variables.

Heroku utilizes its built-in PostgreSQL database for django applications. For the local environment, PostgresSQL had to be installed and the configuaration were provided in the `settings.py` of the project. For deployment, django utilizes the `dj-database-url` to parse the database configuration from Heroku in the app.

For the front-end, Vue JS has been utilized. The following command was performed to initiate the Vue project at the root:

```
vue create src-vue
```

A `vue.config.js` file was created inside the `src-vue` folder in order to tell Vue to generate the production files at a desired location:

```javascript
module.exports = {
  outputDir: "../staticfiles"
};
```

The `settings.py` has been configured in a way that django looks for the front-end contents inside the `templates` folder, which looks for the static files inside the `staticfiles` folder at the root of the prject.

In order to deploy the project, three files were needed to be generated, the contents of which are the following:

- `requirements.txt`: the packages required by this project.

```
astroid==2.2.5
autopep8==1.4.4
dj-database-url==0.5.0
Django==2.2.3
django-braces==1.13.0
djangorestframework==3.9.4
gunicorn==19.9.0
isort==4.3.21
lazy-object-proxy==1.4.1
mccabe==0.6.1
pep8==1.7.1
psycopg2-binary==2.8.3
pycodestyle==2.5.0
pylint==2.3.1
python-decouple==3.1
pytz==2019.1
six==1.12.0
sqlparse==0.3.0
typed-ast==1.4.0
whitenoise==4.1.2
wrapt==1.11.2
```

- `runtime.txt`: The version of python that the project is running on.

```
python-3.6.8
```

- `Procfile`

```
web: gunicorn src.wsgi --log-file -
```

Finally, the following commands were run to deploy the project:

```bash
heroku create favoritethingsmutasim
```

This returned the following URL: `https://favoritethingsmutasim.herokuapp.com`. this URL has been included in the `settings.py` file:

```python
ALLOWED_HOSTS = ['favoritethingsmutasim.herokuapp.com', 'localhost']
```

The following commands were run afterwards:

```bash
git init

heroku git:remote -a favoritethingsmutasim

git add .
git commit -m "Commit message"

heroku config:set DISABLE_COLLECTSTATIC=1

git push heroku master

heroku run python manage.py migrate
```

After these steps, the deployed application can be visited at: https://favoritethingsmutasim.herokuapp.com
