from src import core


def test_sum_this():
    x = range(3)
    assert core.sum_this(x) == 3
