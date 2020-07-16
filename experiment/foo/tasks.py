from celery import shared_task

@shared_task
def hello_punjabi(arg):
    print("A Task is being spawned")
    print(arg)