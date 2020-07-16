from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fulfillment.settings')

app = Celery(
    "fulfillment.celery",
    #backend = 'db+sqlite:///results.sqlite',
    backend = 'redis://localhost:6379/0',
    broker = 'redis://localhost:6379/0'
    #broker = 'sqla+sqlite:///celerydb.sqlite'
)
app.config_from_object('fulfillment.celery')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task
def say_hello():
    print("hello")
# @app.task
# def hello_punjabi(arg):
#     print("A Task is being spawned")
#     print(arg)
#






