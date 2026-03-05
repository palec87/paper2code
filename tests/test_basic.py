"""Basic tests for package_name package."""

import src


def test_hello() -> None:
    """Test the hello function."""
    result = src.hello()
    assert isinstance(result, str)
    assert "Hello from package_name!" == result


def test_package_has_version() -> None:
    """Test that the package has a version attribute."""
    assert hasattr(src, "__version__")
