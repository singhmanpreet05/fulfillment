from __future__ import absolute_import, unicode_literals
from kitchen.usecases.place_operations import *

class AttemptIfHasExpiredOrder:
    def __call__(self, order, shelf_name, capacity):
        # if shelf is full then check any expired order on that shelf
        shelf_orders = GetOrders(shelf_name)
        if len(shelf_orders) == capacity:
            for shelf_order in shelf_orders:
                if Order(shelf_order).is_expired(shelf_name):
                    if AttemptReplacingExpired()(shelf_name, shelf_order, order):
                        return True
        return False

class AttemptIfHasSpace:
    def __call__(self, order, shelf_name, capacity):
        # if there is room in the shelf
        cur_count = GetOrdersLen(shelf_name)
        if cur_count < capacity:
            if AttemptPlacing()(order, shelf_name, capacity):
                return True
        return False

class AttmeptIfMovePossible:
    def __call__(self, order, shelf_name, capacity):
        any_shelf_orders = GetOrders(shelf_name)
        for any_shelf_order in any_shelf_orders:
            exact_shelf_name = Shelf.from_temp(any_shelf_order["temp"])
            exact_shelf_capacity = Shelf.capacity(shelf_name)
            is_replaced = AttemptReplacingExpired()(exact_shelf_name, exact_shelf_capacity, any_shelf_order)
            if is_replaced:
                if AttemptPlacing()(order, shelf_name, capacity):
                    return True
        return False


class ForcePlace:
    def __call__(self, order, shelf_name, capacity):
        while True:
            order = RemoveOrder(shelf_name)
            RemoveOrder()(shelf_name, order)
            if AttemptPlacing(order, shelf_name, capacity):
                return True
            return False







