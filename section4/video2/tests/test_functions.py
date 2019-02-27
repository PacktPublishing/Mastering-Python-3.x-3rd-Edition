import pytest
import functions


def test_add_integers():
    assert functions.add((1, 1)) == 2
    assert functions.add((1, -1)) == 0
    assert functions.add((2 ** 31, 1)) == 2147483649
    # Uncomment to cause this test to fail
    #assert functions.add((2 ** 31, 1)) <= 0


def test_add_strings():
    assert functions.add(("hail", "fellow")) == "hailfellow"
    assert functions.add(("well", "met")) == "wellmet"
    assert functions.add(("", "")) == ""
    with pytest.raises(TypeError):
        functions.add(("bad", 1))
    with pytest.raises(TypeError):
        functions.add((1, "bad"))

def test_even_integers():
    assert functions.even(0)
    assert not functions.even(1)
    assert functions.even(999999999998)
    assert not functions.even(9999999999999)


def test_even_strings():
    assert functions.even("test")
    assert not functions.even("hello")


def test_map(mocker):
    func = mocker.Mock(return_value = 9)

    assert functions.map(func, [1, 2, 3, 4, 5]) == [9, 9, 9, 9, 9]

    func.assert_has_calls([
        mocker.call(1),
        mocker.call(2),
        mocker.call(3),
        mocker.call(4),
        mocker.call(5),
    ])

def test_filter(mocker):
    yes = mocker.Mock(return_value = True)
    no = mocker.Mock(return_value = False)

    assert functions.filter(yes, [1, 2, 3]) == [1, 2, 3]
    assert functions.filter(no, [1, 2, 3]) == []
