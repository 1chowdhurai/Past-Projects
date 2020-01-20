"""CSC148 Assignment 1: Sample tests

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 1.

Warning: This is an extremely incomplete set of tests!

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

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
from simulation import GroceryStoreSimulation

CONFIG_FILE = '''{
  "regular_count": 1,
  "express_count": 0,
  "self_serve_count": 0,
  "line_capacity": 1
}
'''

EVENT_FILE = '''10 Arrive Tamara Bananas 7
5 Arrive Jugo Bread 3 Cheese 3
'''

CONFIG_FILE1 = '''{
"regular_count": 1,
"express_count": 0,
"self_serve_count": 1,
"line_capacity": 3
}
'''

EVENT_FILE1 = '''0 Arrive Felicia Bananas 1 
0 Arrive Pablo Oranges 1
0 Arrive Steve Gum 1
0 Arrive Bob Gum 1
0 Arrive Chad Gum 1
1 Close 0
'''

CONFIG_FILE2 = '''{
"regular_count": 0,
"express_count": 1,
"self_serve_count": 1,
"line_capacity": 3
}
'''

EVENT_FILE2 = '''0 Arrive Felicia A 1 A 1 A 1 A 1 A 1 A 1 A 1 A 1
0 Arrive Bob Apple 1
'''


def test_simulation() -> None:
    """Test two events and single checkout simulation."""
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE))
    stats = gss.run(StringIO(EVENT_FILE))
    assert stats == {'num_customers': 2, 'total_time': 18, 'max_wait': 8}


def test_regular_line() -> None:
    config_file = open('input_files/config_100_10.json')
    sim = GroceryStoreSimulation(config_file)
    config_file.close()
    event_file = open('input_files/events_one.txt')
    sim_stats = sim.run(event_file)
    event_file.close()
    assert sim_stats == {'num_customers': 1, 'total_time': 41, 'max_wait': 31}


def test_express_line() -> None:
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE2))
    stats = gss.run(StringIO(EVENT_FILE2))
    assert stats == {'num_customers': 2, 'total_time': 16, 'max_wait': 16}


def test_self_serve_line() -> None:
    config_file = open('input_files/config_001_10.json')
    sim = GroceryStoreSimulation(config_file)
    config_file.close()
    event_file = open('input_files/events_one.txt')
    sim_stats = sim.run(event_file)
    event_file.close()
    assert sim_stats == {'num_customers': 1, 'total_time': 72, 'max_wait': 62}


def test_one_close() -> None:
    gss = GroceryStoreSimulation(StringIO(CONFIG_FILE1))
    stats = gss.run(StringIO(EVENT_FILE1))
    assert stats == {'num_customers': 5, 'total_time': 8, 'max_wait': 8}


def test_all_events_run() -> None:
    config_file = open('input_files/config_642_05.json')
    sim1 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file1 = open('input_files/events_base.txt')
    stats1 = sim1.run(event_file1)
    event_file1.close()

    config_file = open('input_files/config_642_05.json')
    sim2 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file2 = open('input_files/events_mixtures.txt')
    stats2 = sim2.run(event_file2)
    event_file2.close()

    config_file = open('input_files/config_642_05.json')
    sim3 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file3 = open('input_files/events_no_express.txt')
    stats3 = sim3.run(event_file3)
    event_file3.close()

    config_file = open('input_files/config_642_05.json')
    sim4 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file4 = open('input_files/events_one.txt')
    stats4 = sim4.run(event_file4)
    event_file4.close()

    config_file = open('input_files/config_642_05.json')
    sim5 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file5 = open('input_files/events_one_at_a_time.txt')
    stats5 = sim5.run(event_file5)
    event_file5.close()

    config_file = open('input_files/config_642_05.json')
    sim6 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file6 = open('input_files/events_one_close.txt')
    stats6 = sim6.run(event_file6)
    event_file6.close()

    config_file = open('input_files/config_642_05.json')
    sim7 = GroceryStoreSimulation(config_file)
    config_file.close()

    event_file7 = open('input_files/events_two.txt')
    stats7 = sim7.run(event_file7)
    event_file7.close()

    print(stats1)
    print(stats2)
    print(stats3)
    print(stats4)
    print(stats5)
    print(stats6)
    print(stats7)

    assert True


if __name__ == '__main__':
    import pytest

    pytest.main(['a1_sample_test.py'])
