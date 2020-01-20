"""CSC148 Assignment 1: Tests for Customer

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the Customer class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import Customer
from store import Item


def test_customer_constructor():
    c = Customer('Bob', [])
    assert c.name == 'Bob' and c._items == [] and c.arrival_time == -1


def test_num_items():
    c1 = Customer('A', [])
    assert c1.num_items() == 0
    c2 = Customer('B', [Item('Banana', 1)])
    assert c2.num_items() == 1
    items = []
    for i in range(1000):
        items.append(Item('apple', 1))
    c3 = Customer('C', items)
    assert c3.num_items() == 1000


def test_get_item_time():
    c1 = Customer('A', [Item('banana', 7), Item('orange', 5)])
    assert c1.get_item_time() == 12

    items = []
    total_time = 0
    for i in range(1000):
        items.append(Item('apple', i))
        total_time += i
    c2 = Customer('B', items)

    assert c2.get_item_time() == total_time


if __name__ == '__main__':
    import pytest

    pytest.main(['test_customer.py'])
