"""CSC148 Assignment 1: Tests for checkout classes

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the checkout classes.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import RegularLine, ExpressLine, SelfServeLine, Customer, Item

regLine = RegularLine(2)
exLine = ExpressLine(2)
selfLine = SelfServeLine(2)


def reset_queues() -> None:
    regLine.queue = []
    exLine.queue = []
    selfLine.queue = []


def test_inits() -> None:
    assert regLine.capacity == 2
    assert exLine.capacity == 2
    assert selfLine.capacity == 2

    assert regLine.is_open
    assert exLine.is_open
    assert selfLine.is_open

    assert regLine.queue == []
    assert exLine.queue == []
    assert selfLine.queue == []


def test_len() -> None:
    assert len(regLine) == 0
    assert len(exLine) == 0
    assert len(selfLine) == 0

    regLine.queue = list(range(100))
    exLine.queue = list(range(100))
    selfLine.queue = list(range(100))

    assert len(regLine) == 100
    assert len(exLine) == 100
    assert len(selfLine) == 100

    reset_queues()


def test_can_accept() -> None:
    assert regLine.can_accept(Customer('Bob', []))
    assert regLine.can_accept(Customer('Bob', []))
    regLine.queue = [Customer('Bob', []), Customer('Bob', [])]
    assert not regLine.can_accept(Customer('Bob', []))

    assert exLine.can_accept(Customer('Bob', []))
    assert exLine.can_accept(Customer('Bob', []))
    exLine.queue = [Customer('Bob', []), Customer('Bob', [])]
    assert not exLine.can_accept(Customer('Bob', []))
    exLine.queue = []
    c = (Customer('Bob', [Item('A', 1), Item('A', 1), Item('A', 1),
                          Item('A', 1), Item('A', 1), Item('A', 1),
                          Item('A', 1), Item('A', 1)]))
    assert not exLine.can_accept(c)

    assert selfLine.can_accept(Customer('Bob', []))
    assert selfLine.can_accept(Customer('Bob', []))
    selfLine.queue = [Customer('Bob', []), Customer('Bob', [])]
    assert not selfLine.can_accept(Customer('Bob', []))

    reset_queues()


def test_accept() -> None:
    c = Customer('Bob', [])
    assert regLine.accept(c)
    assert regLine.queue[0].name == 'Bob'
    assert regLine.queue[0]._items == []

    assert exLine.accept(Customer('Bob', []))
    assert exLine.queue[0].name == 'Bob'
    assert exLine.queue[0]._items == []

    assert selfLine.accept(Customer('Bob', []))
    assert selfLine.queue[0].name == 'Bob'
    assert selfLine.queue[0]._items == []

    reset_queues()


def test_start_checkout():
    regLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    assert regLine.start_checkout() == 3
    exLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    assert exLine.start_checkout() == 3
    selfLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    assert selfLine.start_checkout() == 6


def test_complete_checkout():
    regLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    exLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    selfLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    assert regLine.complete_checkout()
    assert exLine.complete_checkout()
    assert selfLine.complete_checkout()
    assert not regLine.complete_checkout()
    assert not exLine.complete_checkout()
    assert not selfLine.complete_checkout()


def test_close():
    regLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    exLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    selfLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    regLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    exLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))
    selfLine.accept(Customer('Bob', [Item('Banana', 1), Item('Orange', 2)]))

    assert len(regLine.close()) == 1
    assert len(exLine.close()) == 1
    assert len(selfLine.close()) == 1
    assert not regLine.is_open
    assert not exLine.is_open
    assert not selfLine.is_open
    assert len(regLine) == 1
    assert len(exLine) == 1
    assert len(selfLine) == 1


if __name__ == '__main__':
    import pytest

    pytest.main(['test_checkouts.py'])
