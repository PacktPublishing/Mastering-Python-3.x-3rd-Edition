import pytest


def test_constructor_distinct():
    from quadtree import QuadTree

    q = QuadTree(width=100, height=100)

    assert abs(q.dimension.real - 100) < 0.0001
    assert abs(q.dimension.imag - 100) < 0.0001

    assert q.branches == [None, None, None, None]
    assert q.children == {}


def test_constructor_complex():
    from quadtree import QuadTree

    q = QuadTree(complex(100, 100))

    assert abs(q.dimension.real - 100) < 0.0001
    assert abs(q.dimension.imag - 100) < 0.0001

    assert q.branches == [None, None, None, None]
    assert q.children == {}


def test_constructor_wrong():
    from quadtree import QuadTree

    with pytest.raises(ValueError):
        QuadTree()

    with pytest.raises(ValueError):
        QuadTree(width=100)

    with pytest.raises(ValueError):
        QuadTree(height=100)

    with pytest.raises(ValueError):
        QuadTree(complex(100, 100), width=100)

    with pytest.raises(ValueError):
        QuadTree(complex(100, 100), height=100)

    with pytest.raises(ValueError):
        QuadTree(complex(100, 100), width=100, height=100)
