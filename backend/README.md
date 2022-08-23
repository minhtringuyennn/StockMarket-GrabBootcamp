## Setup

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Run server:

```sh
(env)$ python3 manage.py runserver
```

By default, Django will use SQLite for database 
