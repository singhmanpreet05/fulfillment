# from __future__ import absolute_import, unicode_literals
# print("chakde tasks")
from celery import shared_task
# from django.conf import settings
# from kitchen.models import *
# import json
from kitchen.usecases import service
# import random
# import redis_lock
#
#
# @shared_task
# def load_orders(filename=settings.ORDERS_FILE):
#     print("load_orders")
#     with open(filename, "r") as file:
#         content = file.read()
#         orders = json.loads(content)
#         service.DestroyKitchen()()
#         service.LoadOrders()(orders[:1])
#
# @shared_task
# def deliver(order_id):
#     service.AttemptRemoving({order_id: "order_id"})
#
#
# @shared_task
# def organizer():
#     print("organizer started")
#     order = service.PickOrderToOrganize()()
#     if not order:
#         return False
#     countdown = random.randrange(2, 7)
#     deliver.apply_async(order["id"], countdown=countdown)
#     if order is not None:
#         temp = order["temp"]
#         shelf_name = Shelf.from_temp(temp)
#         capacity = Shelf.capacity(shelf_name)
#
#         if service.AttemptIfHasSpace()(order, shelf_name, capacity):
#             return True
#         if service.AttemptIfHasExpiredOrder()(order, shelf_name, capacity):
#             return True
#         if service.AttemptIfHasSpace()(order, Shelf.ANY, Shelf.capacity(Shelf.ANY)):
#             return True
#         if service.AttemptIfHasExpiredOrder()(order, Shelf.ANY, Shelf.capacity(Shelf.ANY)):
#             return True
#         if service.AttmeptIfMovePossible(order, Shelf.ANY, Shelf.capacity(Shelf.ANY)):
#             return True
#         return service.ForcePlace(order, Shelf.ANY, Shelf.capacity(Shelf.ANY))
#
@shared_task
def organizers_generator(count):
    print("organizer generator started")
    # for i in range(count):
    #     organizer.delay()
#
#
# # @celery_app.on_after_configure.connect
# # def setup_periodic_tasks(sender, **kwargs):
# #     print("balle")
# #     sender.add_periodic_task(1, say_hello.s('hello'), name='add every 1')
#
