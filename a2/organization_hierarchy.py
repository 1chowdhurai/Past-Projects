"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh

Implemented by Raiyaan Rahman
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO, Tuple


# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """

    i, j = 0, 0
    res = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            res.append(lst1[i])
            i += 1
        else:
            res.append(lst2[j])
            j += 1
    if i < len(lst1):
        res.extend(lst1[i:])
    elif j < len(lst2):
        res.extend(lst2[j:])

    return res


def _sort_by_rating(subordinates: List[Employee], subordinate: Employee) -> \
        List[Employee]:
    """Inserts a subordinate into a list of employees (can also be empty)
    and sorts them according to their rating (from lowest to highest)"""
    inserted = False
    i = 0
    while not inserted and i < len(subordinates):
        if subordinate.rating < subordinates[i].rating:
            subordinates.insert(i, subordinate)
            inserted = True
            break
        i += 1
    if not inserted:
        subordinates.append(subordinate)
    return subordinates


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    - _subordinates are stored by id in ascending order
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._superior = None
        self._subordinates = []

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        return self.eid < other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """

        return self._subordinates

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """
        res = []
        for subordinate in self._subordinates:
            res = merge(res, subordinate.get_all_subordinates())
            res = merge(res, [subordinate])
        return res

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        if self._superior is not None:
            return self._superior.get_organization_head()
        return self

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        return self._superior

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """

        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
        if superior is not None:
            superior.add_subordinate(self)

        self._superior = superior

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> e2.get_direct_subordinates()
        []
        >>> e1.get_superior() is e2
        True
        """
        for subordinate in self._subordinates:
            if subordinate.eid == eid:
                self._subordinates.remove(subordinate)
                break

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """

        if len(self._subordinates) == 0:
            self._subordinates.append(subordinate)

        else:
            inserted = False
            for i in range(len(self._subordinates)):
                if self._subordinates[i].eid > subordinate.eid:
                    self._subordinates.insert(i, subordinate)
                    inserted = True
                    break
            if not inserted:
                self._subordinates.append(subordinate)

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        if self.eid == eid:
            return self
        else:
            for subordinate in self.get_all_subordinates():
                if subordinate.eid == eid:
                    return subordinate
            return None

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        res = []
        for subordinate in self.get_all_subordinates():
            if subordinate.salary > amount:
                res.append(subordinate)
        if self.salary > amount:
            res = merge(res, [self])
        return res

    def get_closest_common_superior(self, eid: int) -> Optional[Employee]:
        """Return the closest common superior in the organization between
        self and the employee with ID <eid>.

        Precondition: <eid> exists in the organization.
        """
        other_employee = self.get_organization_head().get_employee(eid)
        superior1 = self.get_superior()
        superior2 = other_employee.get_superior()

        if superior1.eid == other_employee.eid:
            return other_employee
        elif superior2.eid == self.eid:
            return self

        while superior1.eid != superior2.eid and superior1 is not None \
                and superior2 is not None:
            if self in superior2.get_all_subordinates():
                superior1 = superior1.get_superior()
            elif other_employee in superior1.get_all_subordinates():
                superior2 = superior2.get_superior()
            else:
                superior1 = superior1.get_superior()
                superior2 = superior2.get_superior()

        if superior1.eid == superior2.eid:
            return superior1
        else:
            return None

    def get_higher_paid_employees(self) -> List[Employee]:
        """Return a list of employees whose salaries are greater than
        this employee's salary"""
        return self.get_organization_head().get_employees_paid_more_than(
            self.salary)

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        if self._superior is None:
            return ''
        return self.get_superior().get_department_name()

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        res = str(self.position)
        superior = self.get_superior()

        department = self.get_department_name()
        if department != '':
            res += f', {department}'

        while superior is not None:
            while not isinstance(superior, Leader):
                superior = superior.get_superior()

            if superior.get_department_name() != department:
                department = superior.get_department_name()
                res += f', {department}'

            superior = superior.get_superior()

        return res

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Employee]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """

        if isinstance(self, Leader):
            return self
        superior = self.get_superior()
        while not isinstance(superior, Leader) and superior is not None:
            superior = superior.get_superior()
        return superior

    def change_department_leader(self) -> Employee:
        """
        Makes this employee the leader of their current department,
        becoming the superior of the current department leader.
        self.current_employee keeps all of their subordinates, in addition
        to gaining the leader as a subordinate.

        If self.current_employee is already a leader or does not belong to a
        department, nothing happens.

        >>> bob = Leader(1, 'Bob', 'CEO', 1000000, 95, 'Some Corp')
        >>> ted = Employee(2, 'Ted', 'CFO', 900000, 90)
        >>> ed = Employee(3, 'Ed', 'Assistant to the CFO', 800000, 80)
        >>> ned = Leader(10, 'Ned', 'Head of Accounting', 800000, 80, \
        'Accounting')
        >>> daisy = Leader(15, 'Daisy', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen = Employee(6, 'Jen', 'Financial Risk Manager', 700000, 75)
        >>> jen.become_subordinate(daisy)
        >>> daisy.become_subordinate(ned)
        >>> ned.become_subordinate(ed)
        >>> ed.become_subordinate(ted)
        >>> ted.become_subordinate(bob)
        >>> head = jen.change_department_leader()
        >>> jen = head.get_employee(6)
        >>> jen.get_department_name()
        'Financial Risk'
        >>> daisy = jen.get_all_subordinates()[0]
        >>> daisy.get_superior().eid
        6
        >>> jen.get_superior().eid
        10
        >>> isinstance(jen, Leader)
        True
        >>> isinstance(daisy, Leader)
        False
        """
        # find leader of current department
        superior = self.get_department_leader()

        if superior is not None and superior.eid != self.eid:
            department_name = superior.get_department_name()
            if isinstance(superior, Leader):
                superior = superior.become_employee()

            new_self = self.become_leader(department_name)
            new_self.become_subordinate(superior.get_superior())
            superior.become_subordinate(new_self)

            return new_self.get_organization_head()
        return self.get_organization_head()

    def become_leader(self, department_name: str) -> Leader:
        """
        If already a leader, changes department to department_name, and returns
        the changed leader.
        If an employee becomes a leader, they are replaced by a leader object
        with the same properties (including superior and subordinates), and the
        new leader is returned

        >>> bob = Leader(1, 'Bob', 'CEO', 1000000, 95, 'Some Corp')
        >>> ted = Employee(2, 'Ted', 'CFO', 900000, 90)
        >>> ed = Employee(3, 'Ed', 'Assistant to the CFO', 800000, 80)
        >>> ned = Leader(10, 'Ned', 'Head of Accounting', 800000, 80, \
        'Accounting')
        >>> daisy = Leader(15, 'Daisy', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen = Leader(6, 'Jen', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen.become_subordinate(daisy)
        >>> daisy.become_subordinate(ned)
        >>> ned.become_subordinate(ed)
        >>> ed.become_subordinate(ted)
        >>> ted.become_subordinate(bob)
        >>> jen = jen.become_leader('Global Trades')
        >>> ted = ted.become_leader('Finance')
        >>> jen.get_department_name()
        'Global Trades'
        >>> isinstance(ted, Leader)
        True
        >>> ted.get_superior().eid
        1
        >>> ted.get_direct_subordinates()[0].eid
        3
        >>> len(ted.get_all_subordinates())
        4
        >>> ed.get_superior().eid
        2
        """

        superior = self._superior
        subordinates = []
        for subordinate in self._subordinates:
            subordinates.append(subordinate)

        if superior is not None:
            superior.remove_subordinate_id(self.eid)

        new_self = Leader(self.eid, self.name, self.position,
                          self.salary, self.rating, department_name)

        for employee in subordinates:
            employee.become_subordinate(new_self)

        new_self.become_subordinate(superior)
        self.eid = -1

        return new_self

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the direct subordinate of this employee with the highest
        rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """

        max_rated = self._subordinates[0]
        for subordinate in self._subordinates:
            if subordinate.rating > max_rated.rating:
                max_rated = subordinate
        return max_rated

    def _swap_up_helper(self) -> Employee:
        """
        To be used for swap up method for employee and after leaeder->Employee/
        Leader swaps in Leader wap up

        """
        superior_department = self._superior.get_department_name()
        new_self = self
        superior = self._superior

        if isinstance(superior, Leader) and not isinstance(self, Leader):
            new_self = self.become_leader(superior_department)
            superior = superior.become_employee()

        my_subordinates = new_self.get_direct_subordinates()
        superior_subs = []
        for sub in superior.get_direct_subordinates():
            superior_subs.append(sub)

        new_self.become_subordinate(superior.get_superior())
        superior.become_subordinate(new_self)

        i = 0
        while len(my_subordinates) > 1:
            if my_subordinates[i].eid != superior.eid:
                my_subordinates[i].become_subordinate(superior)
                i = 0
            else:
                i += 1

        i = 0
        while len(superior_subs) > 1:
            if superior_subs[i].eid != new_self.eid:
                superior_subs[i].become_subordinate(new_self)
                superior_subs.remove(superior_subs[i])
                i = 0
            else:
                i += 1

        superior_position = superior.position
        superior.position = new_self.position
        new_self.position = superior_position

        superior_salary = superior.salary
        superior.salary = new_self.salary
        new_self.salary = superior_salary

        return new_self

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """

        return self._swap_up_helper()

    def obtain_subordinates(self, ids: List[int]) -> Employee:
        """Set the employees with IDs in ids as subordinates of
        self.current_employee.

        If those employees have subordinates, the superior of those subordinates
        becomes the employee's original superior.

        If the head is taken as a subordinate, the highest rated subordinate of
        the head becomes the new head (smallest eid taken if multiple employees
        with the same rating)

        returns the head of the organization

        Pre-condition: self.current_employee's id is not in ids.
        """
        subordinates = []
        head = self.get_organization_head()
        for eid in ids:
            subordinates.append(self.get_organization_head().get_employee(eid))

        for subordinate in subordinates:
            if subordinate == head:

                new_head =\
                    self.get_organization_head().get_highest_rated_subordinate()
                self.get_organization_head().remove_subordinate_id(new_head.eid)
                new_head.become_subordinate(None)

                while len(subordinate.get_direct_subordinates()) > 0:
                    subordinate.get_direct_subordinates()[0].become_subordinate(
                        new_head)
                subordinate.become_subordinate(self)
                head = new_head
            else:

                subordinate.become_subordinate(self)

        return head


class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        self._head = head

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        if self._head is None:
            return None
        return self._head.get_employee(eid)

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        if self._head is None:
            self._head = employee
        elif superior_id is None:
            self._head.become_subordinate(employee)
            self._head = employee
        else:
            superior = self._head.get_employee(superior_id)
            employee.become_subordinate(superior)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0.0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """

        avg = 0
        num = 0
        if self._head is None:
            return 0.0
        elif self._head.position == position or position is None:
            avg += self._head.salary
            num += 1
        subordinates = self._head.get_all_subordinates()
        for subordinate in subordinates:
            if subordinate.position == position or position is None:
                avg += subordinate.salary
                num += 1

        if num == 0:
            return 0.0
        return avg / num

    def get_employees_with_position(self, position: str) -> List[Employee]:
        """Returns a list of employees with this position"""
        res = []
        subordinates = self._head.get_all_subordinates()

        for subordinate in subordinates:
            if subordinate.position == position:
                res.append(subordinate)

        if self._head.position == position:
            res = merge(res, [self._head])

        return res

    def get_next_free_id(self) -> int:
        """Return the lowest unused eid in the organization > 0"""
        subordinates = self._head.get_all_subordinates()
        if len(subordinates) == 0:
            return self._head.eid + 1
        else:
            return subordinates[len(subordinates) - 1].eid + 1

    # === TASK 3 ===

    # === TASK 4 ===

    def get_head(self) -> Optional[Employee]:
        """returns the head of the organization, or None if there is no head"""
        return self._head

    def set_head(self, new_head: Employee) -> None:
        """Sets the new head of the organization."""
        self._head = new_head

    def fire_employee(self, eid: int) -> None:
        """Fire the employee with ID eid from self.current_organization.

        Pre-condition: there is an employee with the eid <eid> in
        self.current_organization.
        """

        employee = self.get_employee(eid)
        employee_subordinate_ids = []

        superior = employee.get_superior()
        subordinates = self._head.get_direct_subordinates()
        if superior is not None:
            for sub in employee.get_direct_subordinates():
                employee_subordinate_ids.append(sub.eid)
            superior.obtain_subordinates(employee_subordinate_ids)
            superior.remove_subordinate_id(employee.eid)
        elif len(subordinates) == 0:
            self._head = None
        else:
            new_head = self._head.get_highest_rated_subordinate()
            self._head.remove_subordinate_id(new_head.eid)
            new_head.become_subordinate(None)
            self._head = new_head

            while len(employee.get_direct_subordinates()) > 0:
                employee.get_direct_subordinates()[0].become_subordinate(
                    new_head)

        employee.eid = -1

    def fire_lowest_rated_employee(self) -> None:
        """Fire the lowest rated employee in self.current_organization.

        If two employees have the same rating, the one with the lowest id
        is fired.
        """
        lowest_rated = self._head

        for subordinate in self._head.get_all_subordinates():
            if subordinate.rating < lowest_rated.rating:
                lowest_rated = subordinate

        self.fire_employee(lowest_rated.eid)

    def fire_under_rating(self, min_rating: int) -> None:
        """Fire all employees with a rating below min_rating.

        Employees should be fired in order of increasing rating: the lowest
        rated employees are to be removed first. Break ties in order of eid.
        """

        subordinates = self._head.get_all_subordinates()
        under_rated = []

        for subordinate in subordinates:
            if subordinate.rating < min_rating:
                under_rated = _sort_by_rating(under_rated, subordinate)

        if self._head.rating < min_rating:
            under_rated = _sort_by_rating(under_rated, self._head)

        for employee in under_rated:
            if self.get_employee(employee.eid) is not None:
                self.fire_employee(employee.eid)

    def promote_employee(self, eid: int) -> None:
        """Promote the employee with the eid <eid> in self.current_organization
        until they have a superior with a higher rating than them or until they
        are the head of the organization.

        Precondition: There is an employee in self.current_organization with
        eid <eid>.
        """

        employee = self.get_employee(eid)
        while employee.get_superior() is not None and \
                employee.rating >= employee.get_superior().rating:
            employee = employee.swap_up()

        self._head = employee.get_organization_head()


# === TASK 2: Leader ===
#
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run
# organization_ui.py, though not all of the buttons will work.


class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """

        Employee.__init__(self, eid, name, position, salary, rating)
        self._department_name = department

    def get_department_name(self) -> str:
        """Returns this leader's department name"""
        return self._department_name

    def become_leader(self, department_name: str) -> Leader:
        """Changes the department of this leader"""
        superior = self._superior
        subordinates = self._subordinates
        self.__init__(self.eid, self.name, self.position,
                      self.salary, self.rating, department_name)
        self._superior = superior
        self._subordinates = subordinates
        return self

    def get_department_employees(self) -> List[Employee]:
        """Returns a list of all employees in this Leader's department

        >>> bob = Leader(1, 'Bob', 'CEO', 1000000, 95, 'Some Corp')
        >>> ted = Employee(2, 'Ted', 'CFO', 900000, 90)
        >>> ed = Employee(3, 'Ed', 'Assistant to the CFO', 800000, 80)
        >>> ned = Leader(10, 'Ned', 'Head of Accounting', 800000, 80, \
        'Accounting')
        >>> daisy = Leader(15, 'Daisy', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen = Leader(6, 'Jen', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen.become_subordinate(daisy)
        >>> daisy.become_subordinate(ned)
        >>> ned.become_subordinate(ed)
        >>> ed.become_subordinate(ted)
        >>> ted.become_subordinate(bob)
        >>> res = ned.get_department_employees()
        >>> res[0].eid
        6
        >>> res[1].eid
        10
        >>> res[2].eid
        15

        """

        res = merge(self.get_all_subordinates(), [self])
        return res

    # === TASK 3 ===

    def swap_up(self) -> Employee:
        """Checks for any Leader -> Employee/Leader changes between
        employee and superior, then swaps employee up"""
        superior_department = self._superior.get_department_name()
        new_self = self
        superior = self._superior

        if isinstance(self, Leader) and isinstance(superior, Leader):
            superior.become_leader(self.get_department_name())
            new_self = self.become_leader(superior_department)
        elif isinstance(self, Leader) and not isinstance(superior, Leader):
            superior.become_leader(self.get_department_name())
            new_self = self.become_employee()
        elif isinstance(superior, Leader):
            new_self = self.become_leader(superior_department)
            superior.become_employee()

        return new_self._swap_up_helper()

    def become_employee(self) -> Employee:
        """Replaces self with an employee with the same properties
        (including subordinates and superior) and returns the new employee

        Pre-condition: self is a Leader.

        >>> bob = Leader(1, 'Bob', 'CEO', 1000000, 95, 'Some Corp')
        >>> ted = Employee(2, 'Ted', 'CFO', 900000, 90)
        >>> ed = Employee(3, 'Ed', 'Assistant to the CFO', 800000, 80)
        >>> ned = Leader(10, 'Ned', 'Head of Accounting', 800000, 80, \
        'Accounting')
        >>> daisy = Leader(15, 'Daisy', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen = Leader(6, 'Jen', 'Financial Risk Manager', 700000, 75, \
         'Financial Risk')
        >>> jen.become_subordinate(daisy)
        >>> daisy.become_subordinate(ned)
        >>> ned.become_subordinate(ed)
        >>> ed.become_subordinate(ted)
        >>> ted.become_subordinate(bob)
        >>> ned = ned.become_employee()
        >>> isinstance(ned, Leader)
        False
        >>> ned.get_superior().eid
        3
        >>> len(ned.get_all_subordinates())
        2
        >>> daisy.get_superior().eid
        10
        >>> ned.get_superior().eid
        3
        >>> assert ned.get_organization_head().get_employee(-1) is None
        """
        superior = self._superior

        if superior is not None:
            self._superior.remove_subordinate_id(self.eid)

        new_self = Employee(self.eid, self.name, self.position, self.salary,
                            self.rating)

        new_self._subordinates = self._subordinates
        new_self.become_subordinate(superior)

        for subordinate in self._subordinates:
            self.remove_subordinate_id(subordinate.eid)
            subordinate.become_subordinate(new_self)

        self.eid = -1

        return new_self

    # === TASK 4 ===


# === TASK 5 ===

#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]


def _get_main_department(head: Employee) -> Tuple[str, Employee]:
    """Helper for create department salary tree: gets the main department
    of this organization"""
    department = ''
    if head.get_department_name() != '':
        return head.get_department_name(), head
    else:
        dep_head = None
        subordinates = head.get_direct_subordinates()
        i = 0
        while department == '' and i < len(subordinates):
            dep_head = subordinates[i]
            department = _get_main_department(subordinates[i])
        return department, dep_head


def _get_avg_salaries_in_dep(dep_head: Employee) -> float:
    """Helper for create department salary tree, obtains the average salary in
    a department"""
    total = dep_head.salary
    num = 1
    for subordinate in dep_head.get_all_subordinates():
        if subordinate.get_department_name() == dep_head.get_department_name():
            total += subordinate.salary
            num += 1
    return total / num


def _get_subdepartments(head: Employee) -> List[DepartmentSalaryTree]:
    """Helper for create department salary tree, gets a list of subdepartments
    in this organization"""
    subdepartments = []
    main_dep = head.get_department_name()
    subordinates = head.get_direct_subordinates()
    for subordinate in subordinates:
        sub_dep, sub_head = _get_main_department(subordinate)
        if sub_dep != main_dep and sub_dep not in subdepartments:
            subdepartments.append(
                DepartmentSalaryTree(
                    sub_dep, _get_avg_salaries_in_dep(sub_head),
                    _get_subdepartments(sub_head)))
    return subdepartments


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """

    if _get_main_department(organization.get_head()) == '':
        return None
    else:
        main_dep, dep_head = _get_main_department(organization.get_head())

        return DepartmentSalaryTree(main_dep,
                                    _get_avg_salaries_in_dep(dep_head),
                                    _get_subdepartments(dep_head))


# === TASK 6 ===

# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """

    with file as csv_file:
        lines = csv_file.readlines()

    o = Organization()
    employees = []

    for line in lines:
        att = line.strip().split(',')
        if len(att) == 7:
            emp = Leader(int(att[0]), att[1], att[2], float(att[3]),
                         int(att[4]), att[6])

            if att[5] != '':
                employees.append((emp, int(att[5])))
            else:
                o.add_employee(emp)

        else:

            emp = Employee(int(att[0]), att[1], att[2], float(att[3]),
                           int(att[4]))
            if att[5] != '':
                employees.append((emp, int(att[5])))
            else:
                o.add_employee(emp)

    i = 0
    while len(employees) > 0:
        superior_id = employees[i][1]
        if o.get_employee(superior_id) is not None:
            o.add_employee(employees[i][0], superior_id)
            employees.remove(employees[i])

        i += 1
        if i >= len(employees):
            i = 0

    return o


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})
