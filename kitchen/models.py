# from django.db import models
# # Create your models here.
# import json
# import time
#
# from django_redis import get_redis_connection
#
# class Shelf:
#     ANY = "any_shelf"
#     HOT = "hot_shelf"
#     FROZEN = "frozen_shelf"
#     COLD = "cold_shelf"
#
#     to_capacity = {
#         "hot_shelf": 10,
#         "cold_shelf": 10,
#         "frozen_shelf": 10,
#         "any_shelf": 15
#     }
#
#     @classmethod
#     def capacity(cls, shelf_name):
#         return cls.to_capacity[shelf_name]
#
#     @classmethod
#     def from_temp(cls, temp):
#         return temp + "_shelf"
#
# class Order:
#     def __init__(self, hash):
#         self.hash = hash
#
#     def cur_value(self, cur_shelf):
#         shelf_life = hash["shelfLife"]
#         decayRate = hash["decayRate"]
#
#         # calculate the start end times
#         exact_start = hash("exactStart", 0)
#         exact_end = hash.get("exactEnd", 0)
#         any_start = hash.get("anyStart", 0)
#         any_end = hash.get("anyEnd", 0)
#         if cur_shelf == "any_temperature":
#             any_end = int(time.time())
#         else:
#             exact_end = int(time.time())
#
#         # calculate value lost
#         exact_age = exact_end - exact_start
#         exact_value_lost = exact_age*1*decayRate
#
#         any_age = any_end - any_start
#         any_value_lost = any_age * 2 * decayRate
#
#         # calculate value left
#         return (shelf_life - exact_value_lost - any_value_lost) / shelf_life
#
#     def is_expired(self, cur_shelf):
#         return self.cur_value(cur_shelf) <= 0
#
# class RedisClient:
#     conn = get_redis_connection("default")
#
#     @classmethod
#     def execute(cls, arg_func):
#         func, key, value_list = arg_func(cls.conn)
#         if value_list and isinstance(value_list[0], dict):
#             value_list = [json.dumps(v) for v in value_list]
#         if key:
#             args = [key, *value_list]
#         else:
#             args = value_list
#         print(args)
#         result = func(*args)
#         if result and isinstance(result, str):
#             print("about to print result", result)
#             return json.loads(result)
