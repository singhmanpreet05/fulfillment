from django.apps import AppConfig
import redis_lock
from kitchen.models import RedisClient
class KitchenConfig(AppConfig):
    name = 'kitchen'

    def ready(self):
        import kitchen.tasks
        print(kitchen.tasks)

        # On application start/restart
        #redis_lock.reset_all(RedisClient.conn)