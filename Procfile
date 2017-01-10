web: newrelic-admin run-program gunicorn --pythonpath="$PWD/history" wsgi:application
worker: python history/manage.py rqworker default