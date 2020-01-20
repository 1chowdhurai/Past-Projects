from organization_hierarchy import merge, Employee, Organization, Leader, \
    create_department_salary_tree, create_organization_from_file


def test_merge():
    lst1 = [1, 3, 5, 7, 9]
    lst2 = [2, 4, 6, 8, 10, 11, 12, 14, 16]
    assert merge(lst1, lst2) == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]

    lst2 = [1, 3, 5, 7, 9]
    lst1 = [2, 4, 5, 6, 10]

    assert merge(lst1, lst2) == [1, 2, 3, 4, 5, 5, 6, 7, 9, 10]


def test_employee_lt():
    bob = Employee(2, 'Bob', 'asd', 123.3, 50)
    emily = Employee(3, 'Emily', 'dsa', 321.1, 30)
    bobo = Employee(2, 'Bobo', 'dsa', 345.3, 40)

    assert bob < emily
    assert not bob < bobo


def test_employee_subordinates():
    bob = Employee(2, 'Bob', 'asd', 123.3, 50)
    emily = Employee(4, 'Emily', 'dsa', 321.1, 30)
    a = Employee(3, 'a', 'hjk', 876.1, 60)
    b = Employee(5, 'b', 'kjh', 456.1, 80)

    bob.add_subordinate(emily)
    bob.add_subordinate(a)

    emily.add_subordinate(b)

    assert emily._superior is None
    assert a._superior is None
    assert b._superior is None

    assert bob.get_direct_subordinates() == [a, emily]
    assert bob.get_all_subordinates() == [a, emily, b]


def test_become_subordinate():
    bob = Employee(2, 'Bob', 'asd', 123.3, 50)
    emily = Employee(4, 'Emily', 'dsa', 321.1, 30)
    a = Employee(3, 'a', 'hjk', 876.1, 60)

    emily.become_subordinate(bob)
    a.become_subordinate(emily)
    assert a.get_superior().eid == emily.eid
    assert emily.get_direct_subordinates()[0].eid == a.eid
    assert bob.get_employee(3).eid == 3


def test_get_average_salary():
    o = Organization()
    bob = Employee(2, 'Bob', 'asd', 123.3, 50)
    emily = Employee(4, 'Emily', 'dsa', 321.1, 30)
    a = Employee(3, 'a', 'hjk', 876.1, 60)

    o.set_head(bob)
    emily.become_subordinate(bob)
    a.become_subordinate(bob)
    assert o.get_average_salary() == (bob.salary + emily.salary + a.salary) / 3


def test_change_department_leader():
    bob = Leader(1, 'Bob', 'CEO', 1000000, 95, 'Some Corp')
    ted = Employee(2, 'Ted', 'CFO', 900000, 90)
    ed = Employee(3, 'Ed', 'Assistant to the CFO', 800000, 80)
    ned = Leader(10, 'Ned', 'Head of Accounting', 800000, 80, 'Accounting')
    daisy = Leader(15, 'Daisy', 'Financial Risk Manager', 700000, 75,
                   'Financial Risk')
    jen = Employee(6, 'Jen', 'Financial Risk Manager', 700000, 75)
    jen.become_subordinate(daisy)
    daisy.become_subordinate(ned)
    ned.become_subordinate(ted)
    ed.become_subordinate(ted)
    ted.become_subordinate(bob)
    head = ted.change_department_leader()
    ted = head.get_employee(2)
    assert ted.get_department_name() == 'Some Corp'
    bob = ted.get_direct_subordinates()[0]
    assert bob.get_superior().eid == 2
    assert ted.get_superior() is None
    assert isinstance(ted, Leader)
    assert not isinstance(bob, Leader)
    assert head.get_employee(-1) is None
    for subordinate in head.get_all_subordinates():
        assert subordinate.eid != -1
    assert ed.get_superior().eid == 2
    assert len(ted.get_all_subordinates()) == 5
    assert len(ted.get_direct_subordinates()) == 3


def test_change_department_leader2():
    bob = Leader(1, 'Bob', 'CEO', 1000000, 95, 'Some Corp')
    ted = Employee(2, 'Ted', 'CFO', 900000, 90)
    ed = Employee(3, 'Ed', 'Assistant to the CFO', 800000, 80)
    ned = Leader(10, 'Ned', 'Head of Accounting', 800000, 80, 'Accounting')
    daisy = Leader(15, 'Daisy', 'Financial Risk Manager', 700000, 75,
                   'Financial Risk')
    jen = Employee(6, 'Jen', 'Financial Risk Manager', 700000, 75)
    jen.become_subordinate(daisy)
    daisy.become_subordinate(ned)
    ned.become_subordinate(ed)
    ed.become_subordinate(ted)
    ted.become_subordinate(bob)
    head = jen.change_department_leader()
    jen = head.get_employee(6)
    assert jen.get_department_name() == 'Financial Risk'
    daisy = jen.get_direct_subordinates()[0]
    assert daisy.get_superior().eid == 6
    assert jen.get_superior().eid == 10
    assert isinstance(jen, Leader)
    assert not isinstance(daisy, Leader)


def test_become_leader():
    ted = Employee(2, 'Ted', 'CFO', 900000, 90)
    ned = Employee(1, 'Ned', 'Accountant', 800000, 80)
    ned.become_subordinate(ted)
    new_ted = ted.become_leader('Some Corp.')
    assert new_ted.get_employee(-1) is None
    for subordinate in new_ted.get_all_subordinates():
        assert subordinate.eid != -1
    assert ted.get_superior() is None
    assert ned.get_superior().eid == 2


def test_fire_employee():
    emp1 = Employee(1, '1', '1', 1, 1)
    emp2 = Employee(2, '2', '2', 2, 2)
    emp3 = Employee(3, '3', '3', 3, 3)
    emp4 = Employee(4, '4', '4', 4, 4)
    emp5 = Employee(5, '5', '5', 5, 5)

    emp2.become_subordinate(emp1)
    emp3.become_subordinate(emp1)
    emp4.become_subordinate(emp3)
    emp5.become_subordinate(emp3)

    o = Organization(emp1)

    o.fire_employee(3)
    assert len(emp1.get_direct_subordinates()) == 3

    o.fire_lowest_rated_employee()
    assert o.get_head().eid == 5
    assert o.get_head().get_superior() is None


def test_fire_under_rated():
    emp1 = Employee(1, '1', '1', 1, 1)
    emp2 = Employee(2, '2', '2', 2, 2)
    emp3 = Employee(3, '3', '3', 3, 3)
    emp4 = Employee(4, '4', '4', 4, 4)
    emp5 = Employee(5, '5', '5', 5, 5)

    emp2.become_subordinate(emp1)
    emp3.become_subordinate(emp1)
    emp4.become_subordinate(emp3)
    emp5.become_subordinate(emp3)

    o = Organization(emp1)
    o.fire_under_rating(3)

    assert o.get_head().eid == 3
    assert len(o.get_head().get_all_subordinates()) == 2
    assert o.get_head().get_superior() is None


def test_promote_employee():
    emp1 = Employee(1, '1', '1', 1, 1)
    emp2 = Employee(2, '2', '2', 2, 2)
    emp3 = Employee(3, '3', '3', 3, 3)
    emp4 = Employee(4, '4', '4', 4, 4)
    emp5 = Employee(5, '5', '5', 5, 5)

    emp2.become_subordinate(emp1)
    emp3.become_subordinate(emp2)
    emp4.become_subordinate(emp3)
    emp5.become_subordinate(emp3)

    emp1 = emp1.become_leader('Some Corp.')
    emp2 = emp2.become_leader('Tech')
    emp4 = emp4.become_leader('Programming')
    o = Organization(emp1)

    o.promote_employee(4)
    assert o.get_head().eid == 4
    emp = o.get_employee(4)
    assert len(emp.get_direct_subordinates()) == 1
    sup = o.get_employee(1)
    assert len(sup.get_direct_subordinates()) == 1
    assert isinstance(emp, Leader)
    assert emp.get_department_name() == 'Some Corp.'
    assert isinstance(sup, Leader)
    assert sup.get_department_name() == 'Tech'


def test_get_closest_common_superior():
    o = create_organization_from_file(open('employees.txt'))
    assert o.get_employee(11).get_closest_common_superior(15).eid == 11
    assert o.get_employee(15).get_closest_common_superior(13).eid == 12
    assert o.get_employee(15).get_closest_common_superior(7).eid == 1


def test_fire_under_rated2():
    o = create_organization_from_file(open('employees.txt'))
    o.fire_under_rating(30)
    assert o.get_head().eid == 7
    assert len(o.get_head().get_direct_subordinates()) == 3


def test_avg_salary_with_position():
    o = create_organization_from_file(open('employees.txt'))
    assert o.get_average_salary('Programmer') == 50000.0


if __name__ == '__main__':
    import pytest

    pytest.main(['test_organization_hierarchy.py'])
