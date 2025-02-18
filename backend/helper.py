import sys, time
import weaviate
from redis import Redis

def wait_for_weaviate_local(port:int=8083, gprc_port:int=50053, timeout:int=60):
  """
  Waits for the Weaviate instance to be ready.

  Args:
    port (int): The port of the local Weaviate instance.
    timeout (int): Maximum time to wait in seconds.

  Returns:
    weaviate.Client: A connected Weaviate client.

  Raises:
    TimeoutError: If Weaviate does not become ready within the timeout period.
  """
  start_time = time.time()

  while True:
    try:
      client = weaviate.connect_to_local(
        host="doc_weaviate",
        port=port
      )

      if client.is_ready():
        print("Weaviate is ready!")
        return client
      else:
        print("Weaviate is not ready yet.")
    except Exception as e:
      print(f"Weaviate connection error: {e}")

    if time.time() - start_time > timeout:
      print("Weaviate did not become ready in time.")
      sys.exit(1)
    
    time.sleep(2)


def wait_for_redis_local(port:int=6379, timeout:int=60):
  """
  Waits for the Redis instance to be ready.

  Args:
    port (int): The port of the local Redis instance.
    timeout (int): Maximum time to wait in seconds.

  Returns:
    redis.Client: A connected Redis client.

  Raises:
    TimeoutError: If Redis does not become ready within the timeout period.
  """
  start_time = time.time()

  while True:
    try:
      client = Redis.from_url(f"redis://doc_redis:{port}")

      if client.ping():
        print("Redis is ready!")
        return client
      else:
        print("Redis is not ready yet.")
    except Exception as e:
      print(f"Redis connection error: {e}")

    if time.time() - start_time > timeout:
      print("Redis did not become ready in time.")
      sys.exit(1)
    
    time.sleep(2)