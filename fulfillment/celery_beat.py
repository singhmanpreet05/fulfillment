from fulfillment.celery import app as celery_app
from fulfillment.celery import say_hello
# from kitchen.tasks import say_hello
from kitchen.tasks import *
# Add periodic tasks
from datetime import timedelta

# CELERYBEAT_SCHEDULE = {
#     "runs-every-1-seconds": {
#         "task": "fulfillment.say_hello",
#         "schedule": timedelta(seconds=1),
#         "args": (1)
#     },
# }
# import crontab
# CELERYBEAT_SCHEDULE = {
#     'add-every-monday-morning': {
#         'task': 'fulfillment.celery.say_hello',
#         'schedule': crontab(minute="*"),
#         'args': (16, 16),
#     },
# }

# print("about to schedule a load orders job")
# load_orders.delay()

# @celery_app.on_after_finalize.connect
# def organizers_generate_task(sender, **kwargs):
#     print("inside organizers_generate_task")
#     task_count = 1
#     sender.add_periodic_task(1, organizers_generator.s(task_count), name="generate_orders")

# @celery_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     load_orders.del

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(1,say_hello.s(), name="balle")



