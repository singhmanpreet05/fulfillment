from kitchen.models import *
import redis_lock
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class GetOrders:
    def __call__(self, shelf_name):
        return RedisClient.execute(lambda conn: (conn.range, shelf_name, [0, -1]))

class GetOrdersLen:
    def __call__(self, shelf_name):
        return RedisClient.execute(lambda conn: (conn.scard, shelf_name, []))

class GetRandomOrder:
    def __call__(self, shelf_name):
        return RedisClient.execute(lambda conn: (conn.srand, shelf_name, []))

class GetShelf:
    def __call__(self, order_id):
        return RedisClient.execute(lambda conn: (conn.get, order_id, []))

class RemoveOrder:
    def __call__(self, shelf_name=None, order=None):
        if order:
            lock = redis_lock.Lock(RedisClient.conn, order["id"])
            if not shelf_name:
                shelf_name = GetShelf(order["id"])
            attempts = 3
            for i in range(attempts):
                if lock.acquire(blocking=False):
                    if shelf_name == RedisClient.execute(lambda conn: (conn.get, order["id"], [])):
                        RedisClient.execute(lambda conn: (conn.srem, shelf_name, [order], []))
                        RedisClient.execute(lambda conn: (conn.delete, order["id"], []))
                        lock.release()
                        logger.info("{} was removed from the shelf {}".format(order["id"], shelf_name))
                        return True
                    else:
                        shelf_name = RedisClient.execute(lambda conn: (conn.get, order["id"], []))
                time.sleep(.01)
            return False
        else:
            removed_order = RedisClient.execute(lambda conn: (conn.spop, shelf_name, []))
            logger.info("{} was removed from the shelf {}".format(removed_order["id"], shelf_name))

class PickOrderToOrganize:
    def __call__(self):
        order = RedisClient.execute(lambda conn: (conn.spop, "orders", []))
        if order:
            logger.info("Order {} picked to organize on desired shelf".format(order["id"]))


class AddOrder:
    def __call__(self, shelf_name, order, redis_lock=redis_lock):
        lock = redis_lock.Lock(RedisClient.conn, order["id"])
        attempts = 3
        for i in range(attempts):
            if lock.acquire(blocking=False):
                RedisClient.execute(lambda conn: (conn.set, order["id"], shelf_name))
                RedisClient.execute(lambda conn: (conn.sadd, shelf_name, [order]))
                logger.info("{} was added to the shelf {}".format(order["id"], shelf_name))
                lock.release()
                return True
            time.sleep(.01)
        return False


class DestroyKitchen:
    def __call__(self):
        #RedisClient.execute(lambda conn: (conn.flushall, None, []))
        logger.info("Order Queue Cleared")

class LoadOrders:
    def __call__(self, orders):
        RedisClient.execute(lambda conn: (conn.sadd, "orders", orders))
        logger.info("{} Orders Loaded".format(len(orders)))