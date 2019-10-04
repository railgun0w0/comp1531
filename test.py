import pytest
class AccessError(Exception):
    pass
def plus(x,y):
    if x < 0 and y < 0:
        raise AccessError
    return x + y

def test_plus():
    with pytest.raises(AccessError):
        plus(-1,-1)