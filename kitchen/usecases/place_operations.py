from __future__ import absolute_import, unicode_literals
import redis_lock
from kitchen.usecases.concrete_operations import *

class AttemptPlacing:
    ATTEMPTS = 3

    def __call__(self, order, shelf_name, capacity, redis_lock=redis_lock):
        lock = redis_lock.Lock(RedisClient.conn, shelf_name)
        for i in range(self.ATTEMPTS):
            if lock.acquire(blocking=False):
                cur_count = GetOrdersLen(shelf_name)
                if cur_count < capacity:
                    AddOrder()(shelf_name, order)
                    lock.release()
                    return True
                # shelf is full
                lock.release()
                return False
            time.sleep(.01)

class AttemptReplacingExpired:
    ATTEMPTS = 3

    def __call__(self, shelf_name, old_order, new_order, redis_lock=redis_lock):
        lock = redis_lock.Lock(RedisClient.conn, shelf_name)
        for i in range(self.ATTEMPTS):
            if lock.acquire(blocking=False):
                exact_shelf_orders_again = GetOrders(shelf_name)
                if old_order in exact_shelf_orders_again:
                    RemoveOrder()(shelf_name, old_order)
                    AddOrder()(shelf_name, new_order)
                    lock.release()
                    return True

                # order got moved before we could force expire it
                lock.release()
                return False
            time.sleep(.01)

class AttemptRemoving:
    attempts = 3

    def __call__(self, order, redis_lock=redis_lock):
        shelf_name = GetShelf(order["id"])
        lock = redis_lock.Lock(RedisClient.conn, shelf_name)
        for i in range(self.ATTEMPTS):
            if lock.acquire(blocking=False):
                if shelf_name == GetShelf(order["id"]):
                    RemoveOrder()(shelf_name, order)
                    lock.release()
                    return True
                lock.release()
                shelf_name = GetShelf(order["id"])
            time.sleep(.01)
        lock.release()
        return False