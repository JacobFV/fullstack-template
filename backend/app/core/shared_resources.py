import redis

import redis

def get_redis_connection():
    """
    Establishes a connection to a Redis server.
    
    Returns:
        redis.Redis: A Redis client instance connected to the Redis server.
    """
    try:
        # Replace 'localhost' and 6379 with your Redis server's host and port if different
        r = redis.Redis(host='localhost', port=6379, db=0)
        return r
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        raise

settings = {
    "database_name": "my_database",
    "api_key": "your_api_key_here",
    "connection_string": "your_connection_string_here"
}
