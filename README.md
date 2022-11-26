# stvme
Database project for uni

# Development guide

## Installation
```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ docker-compose up -d database
$ python manage.py migrate --fake-initial && \
    python manage.py runserver
```

## Todo List
- [ ] Use Celery and Redis for profile-change's events and assigning orders.
- [ ] Complete models' field values such as verbose_name lables etc ...
- [ ] Develope front codes.
- [ ] Write test cases.
- [ ] Support for localization.
- [ ] Write documents.