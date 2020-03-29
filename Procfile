release: python workatolist/manage.py migrate
release: python workatolist/manage.py importauthors "authors.csv"
web: gunicorn --chdir workatolist workatolist.wsgi