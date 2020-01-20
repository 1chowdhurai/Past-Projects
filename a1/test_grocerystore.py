"""CSC148 Assignment 1: Tests for GroceryStore

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the GroceryStore class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from io import StringIO
from store import GroceryStore, RegularLine, ExpressLine, SelfServeLine, \
    Customer, Item

# TODO: write your test functions for GroceryStore here
# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.
CONFIG_FILE = '''{
  "regular_count": 2,
  "express_count": 2,
  "self_serve_count": 2,
  "line_capacity": 5
}
'''

store = GroceryStore(StringIO(CONFIG_FILE))


def test_init() -> None:
    for i in range(len(store._lines)):
        if i < 2:
            assert isinstance(store._lines[i], RegularLine)
        elif i < 4:
            assert isinstance(store._lines[i], ExpressLine)
        else:
            assert isinstance(store._lines[i], SelfServeLine)
        assert store._lines[i].capacity == 5


def test_enter_line() -> None:
    for i in range(len(store._lines)):
        assert store.enter_line(Customer('Bob', [])) == i

    c = Customer('Bob', [Item('A', 1), Item('A', 1), Item('A', 1), Item('A', 1),
                         Item('A', 1), Item('A', 1), Item('A', 1),
                         Item('A', 1)])
    for i in range(4):
        if i < 2:
            assert store.enter_line(c) == i
        else:
            assert store.enter_line(c) == i + 2


def test_line_is_ready() -> None:
    store._lines[0].queue = [Customer('Bob', [Item('A', 1)])]
    assert store.line_is_ready(0)
    store._lines[0].accept(Customer('Bob', []))
    assert not store.line_is_ready(0)


def test_start_checkout() -> None:
    assert store.start_checkout(0) == 1
    store._lines[2].queue = [Customer('Bob', [Item('A', 1)])]
    assert store.start_checkout(2) == 1
    store._lines[4].queue = [Customer('Bob', [Item('A', 1)])]
    assert store.start_checkout(4) == 2


def test_complete_checkout() -> None:
    store._lines[0].queue = [Customer('Bob', [Item('A', 1)])]
    assert not store.complete_checkout(0)
    assert len(store._lines[0]) == 0

    store._lines[0].queue = [Customer('Bob', [Item('A', 1)]),
                             Customer('Bob', [Item('A', 1)])]
    assert store.complete_checkout(0)
    assert len(store._lines[0]) == 1


def test_close_line() -> None:
    store._lines[0].queue = [Customer('Bob', [Item('A', 1)]),
                             Customer('Bob', [Item('A', 1)])]
    assert len(store.close_line(0)) == 1
    assert not store._lines[0].is_open


def test_get_first_in_line() -> None:
    store._lines[0].queue = [Customer('Bob', [Item('A', 1)]),
                             Customer('Anne', [Item('B', 2)])]
    c = store.get_first_in_line(0)
    assert c.name == 'Bob'
    assert c._items[0].name == 'A'
    assert c._items[0].get_time() == 1


if __name__ == '__main__':
    import pytest

    pytest.main(['test_grocerystore.py'])
