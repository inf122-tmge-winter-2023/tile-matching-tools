import pytest

from tilematch_tools import gimme_five

def test_vacuous():
    """A test the passes vacuously"""
    pass

@pytest.mark.parametrize("owed, final", [
    (0, 5),
    (1, 4),
    (2, 3),
    (3, 2),
    (4, 1),
    (5, 0)
])
def test_gimme_five(owed, final):
    """Test the gimme five sample function"""
    assert gimme_five() - owed == final

def test_exception_is_raised():
    """Test that an exception is raised"""
    with pytest.raises(ValueError):
        raise ValueError
