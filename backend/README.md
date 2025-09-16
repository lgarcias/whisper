# Backend (quick start)

Instructions to avoid Python import errors and run the backend.

Quick recommendations

- Run the app as a module or with `uvicorn` from the repository root so relative imports work:

```bash
# From the repository root
uvicorn backend.app.main:app --reload
```

- To start an RQ worker (from the repository root):

```bash
# Make sure `PYTHONPATH` points at the project root if you haven't installed the package
PYTHONPATH=. rq worker whisper
```

- Do not run files inside `backend/app/` with `python backend/app/main.py` if you use relative imports (e.g. `from .config import settings`) — use `-m` or `uvicorn` instead.

Dependencies

- Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Renamed `queue.py`

- The file previously named `backend/app/queue.py` has been renamed internally to `backend/app/rq_queue.py` to avoid shadowing the standard library. The main code now imports from `rq_queue`.

If you need to expose `backend.app.queue` for external compatibility, create a small shim that re-exports `queue` from `rq_queue`.
