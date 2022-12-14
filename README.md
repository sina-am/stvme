# stvme
Database project for uni

# Development guide

## Installation
For running the project using docker:
```
docker-compose -f docker-compose-all.yml up --build
```

To debug project and work with it. it's better to only run the external services using docker.
And use local machine to run Django.
```
$ docker-compose up
$ python -m venv .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
(.venv)$ python manage.py migrate --fake-initial && \
    python manage.py runserver
```

If you also want to run celery workers (which is used for order suggestion) 
```
(.venv)$ celery -A config worker -l INFO
```
## Todo List
- [ ] Use Celery and Redis for profile-change's events and assigning orders.
- [ ] Complete models' field values such as verbose_name lables etc ...
- [ ] Develope front codes.
- [ ] Write test cases.
- [ ] Support for localization.
- [ ] Write documents.