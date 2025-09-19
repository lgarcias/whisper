# tests/test_worker.py
from backend.app import worker as worker_mod


class FakeWorker:
    """A dummy Worker that tracks init and work()."""
    constructed_with = None
    worked = False
    with_scheduler = None

    def __init__(self, queues, connection=None):
        FakeWorker.constructed_with = queues
        # keep signature compatible with Worker(..., connection=redis)
        self.connection = connection

    def work(self, with_scheduler=False):
        FakeWorker.worked = True
        FakeWorker.with_scheduler = with_scheduler
        return True


def test_run_initializes_worker_and_calls_work(monkeypatch):
    # Patch only Worker (no Connection used in worker.py anymore)
    monkeypatch.setattr(worker_mod, "Worker", FakeWorker)

    # Run entrypoint
    worker_mod.run()

    # Assertions
    assert FakeWorker.constructed_with is not None
    assert worker_mod.queue in FakeWorker.constructed_with
    assert FakeWorker.worked is True
    assert FakeWorker.with_scheduler is True
