from oware.model.board import Board, _counterclockwise

def test_counterclockwise():
    assert list(_counterclockwise(0, 3)) == [1, 2, 3]
