from celery import Celery
app = Celery(
    "punjabi",
    backend = 'db+sqlite:///results.sqlite',
    broker = 'sqla+sqlite:///celerydb.sqlite'
)

#app.config_from_object("punjabi")
from foo.tasks import *


#hello_punjabi.delay(4)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print("balle")
    sender.add_periodic_task(1, hello_punjabi.s('hello'), name='add every 1')

# from datetime import timedelta
# CELERYBEAT_SCHEDULE = {
#     'every-second': {
#         'task': 'punjabi_server.hello_punjabi',
#         'schedule': timedelta(seconds=1),
#     },
# }
#
# app.finalize()
# print("End of file")





