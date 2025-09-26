import pytest
from rq import Queue
from redis import Redis
from backend.app import rq_queue


def test_redis_instance():
    assert isinstance(rq_queue.redis, Redis)


def test_queue_instance():
    assert isinstance(rq_queue.queue, Queue)
    assert rq_queue.queue.name == "whisper"
    assert rq_queue.queue.connection == rq_queue.redis
