import os
import redis.asyncio as redis
from dotenv import load_dotenv

load_dotenv()

REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.from_url(f"redis://localhost:{REDIS_PORT}", decode_responses=True)
