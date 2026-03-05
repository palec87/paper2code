"""Basic tests for paper2code package."""

import src.paper2code as paper2code


def test_hello() -> None:
    """Test the hello function."""
    result = paper2code.hello()
    assert isinstance(result, str)
    assert "Hello from paper2code!" == result


def test_package_has_version() -> None:
    """Test that the package has a version attribute."""
    assert hasattr(paper2code, "__version__")
