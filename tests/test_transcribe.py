import pytest
from backend.app import transcribe


def test_pick_device_auto_cpu(monkeypatch):
    monkeypatch.setattr("builtins.__import__", lambda name, *args, **kwargs: __import__(name, *args, **kwargs) if name !=
                        "torch" else type("torch", (), {"cuda": type("cuda", (), {"is_available": staticmethod(lambda: False)})})())
    assert transcribe.pick_device("auto") == "cpu"


def test_pick_device_auto_cuda(monkeypatch):
    class FakeTorch:
        class cuda:
            @staticmethod
            def is_available():
                return True
    monkeypatch.setitem(__import__("sys").modules, "torch", FakeTorch)
    assert transcribe.pick_device("auto") == "cuda"
    __import__("sys").modules.pop("torch")


def test_pick_device_explicit_cpu():
    assert transcribe.pick_device("cpu") == "cpu"


def test_pick_device_explicit_cuda(monkeypatch):
    class FakeTorch:
        class cuda:
            @staticmethod
            def is_available():
                return True
    monkeypatch.setitem(__import__("sys").modules, "torch", FakeTorch)
    assert transcribe.pick_device("cuda") == "cuda"
    __import__("sys").modules.pop("torch")
