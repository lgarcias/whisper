# backend/app/worker.py
from rq import Worker

from . import transcribe  # noqa: F401 (ensure task module is imported)
from .rq_queue import queue, redis  # shared Redis connection and queue


def run() -> None:
    """Start an RQ worker listening to the 'whisper' queue."""
    worker = Worker([queue], connection=redis)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    run()
