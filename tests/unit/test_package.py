import peermock


def test_package_version() -> None:
    assert peermock.__version__ == "0.1.0"
