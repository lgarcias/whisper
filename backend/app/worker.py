# backend/app/worker.py
from rq import Worker
from .rq_queue import redis, queue  # shared Redis connection and queue
from . import transcribe  # noqa: F401 (ensure task module is imported)


def run() -> None:
    """Start an RQ worker listening to the 'whisper' queue."""
    worker = Worker([queue], connection=redis)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    run()
