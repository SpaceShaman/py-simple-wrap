import pytest
from py_simple_package.src.py_simple.easy_random import (
    roll_dice,
    flip_coin,
    pick_random_item,
    shuffle_list,
    random_int,
)


def test_roll_dice():
    for _ in range(50):
        res = roll_dice(6)
        assert 1 <= res <= 6

    with pytest.raises(ValueError):
        roll_dice(0)


def test_flip_coin():
    outcomes = {flip_coin() for _ in range(50)}
    assert outcomes.issubset({"Heads", "Tails"})


def test_pick_random_item():
    items = ["apple", "banana", "cherry"]
    for _ in range(20):
        assert pick_random_item(items) in items

    with pytest.raises(ValueError):
        pick_random_item([])


def test_shuffle_list():
    original = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    shuffled = shuffle_list(original)
    assert len(shuffled) == len(original)
    assert set(shuffled) == set(original)
    assert original == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    assert shuffle_list([]) == []

def test_random_int():
    for _ in range(50):
        val = random_int(5, 15)
        assert 5 <= val <= 15

    with pytest.raises(ValueError):
        random_int(10, 5)
