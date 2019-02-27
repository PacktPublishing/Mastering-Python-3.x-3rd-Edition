from oware.model.board import Board, _counterclockwise

def test_counterclockwise():
    assert list(_counterclockwise(0, 3)) == [1, 2, 3]

def test_counterclockwise_wrap():
    assert list(_counterclockwise(2, 15)) == [3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1, 3, 4, 5, 6]

def test_houses_for_player():
    board = Board()
    board.houses = list(range(12))

    assert list(board.houses_for_player(0)) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert list(board.houses_for_player(1)) == [6, 7, 8, 9, 10, 11, 0, 1, 2, 3, 4, 5]

def test_player_has_seeds():
    board1 = Board()
    board2 = Board()

    board1.houses = [0] * 12
    board1.houses[4] = 1

    board2.houses = [0] * 12
    board2.houses[10] = 1

    assert board1.player_has_seeds(0)
    assert not board1.player_has_seeds(1)

    assert not board2.player_has_seeds(0)
    assert board2.player_has_seeds(1)

def test_after_move_simple():
    before = Board() # All the houses contain 4 seeds
    after = before.after_move(0, 4)

    assert after.houses[4] == 0
    assert after.houses[5] == 5
    assert after.houses[6] == 5
    assert after.houses[7] == 5
    assert after.houses[8] == 5

def test_after_move_can_not_capture():
    before = Board()
    before.houses = [0] * 12
    before.houses[3] = 4
    before.houses[6] = 1
    before.houses[7] = 1

    after = before.after_move(0, 3)

    assert after.houses[3] == 0
    assert after.houses[4] == 1
    assert after.houses[5] == 1
    assert after.houses[6] == 2
    assert after.houses[7] == 2
    assert after.captured[0] == 0

def test_sow_simple():
    before = Board()

    after = before.sow(0, 4)

    assert after.houses[4] == 0
    assert after.houses[5] == 5
    assert after.houses[6] == 5
    assert after.houses[7] == 5
    assert after.houses[8] == 5

def test_sow_complex_valid():
    before = Board()
    before.houses = [0] * 12
    before.houses[0] = 9
    before.houses[1] = 2

    after = before.sow(0, 0)

    assert not after.valid_moves
    assert after.houses[8] == 1

def test_sow_complex_invalid():
    before = Board()
    before.houses = [0] * 12
    before.houses[0] = 9
    before.houses[1] = 2

    after = before.sow(0, 1)

    assert after.valid_moves == [0]
