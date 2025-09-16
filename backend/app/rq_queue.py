from rq import Queue
from redis import Redis
from .config import settings

redis = Redis.from_url(settings.REDIS_URL)
queue = Queue("whisper", connection=redis)
