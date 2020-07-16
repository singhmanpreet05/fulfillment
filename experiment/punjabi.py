from celery import Celery
from celery import shared_task
app = Celery(
    "punjabi",
    backend = 'db+sqlite:///results.sqlite',
    broker = 'sqla+sqlite:///celerydb.sqlite'
)
app.config_from_object("punjabi")

app.autodiscover_tasks(["foo"])

# @app.task
# def hello_punjabi(arg):
#     print("A Task is being spawned")
#     print(arg)

#app.finalize()

