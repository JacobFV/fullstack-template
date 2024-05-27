import redis

import redis

def get_redis_connection():
   
   # redis logic here put here later

    try:
        # Replace 'localhost' and 6379 with your Redis server's host and port if different
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise

settings = {
#
}
