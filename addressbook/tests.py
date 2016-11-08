import os
import unittest

from addressbook.core import (
        AddressBook, 
        Group, 
        Person,
        ValidationError
)
from .tst import Node

class ABTest(unittest.TestCase):

    def setUp(self):
        self.ab = AddressBook('test.dat')
        self.person = Person(
                'Test', 'Person', 'Test address',
                '+18005555555', 'test@example.com')
        self.group = Group('Test group')

    def tearDown(self):
        os.remove('test.dat')

    def test_ab_add_person(self):
        self.assertEqual(len(self.ab._book), 0)
        self.ab.add(self.person)
        self.assertEqual(len(self.ab._book), 1)

    def test_create_person_fail_phone(self):
        self.assertEqual(len(self.ab._book), 0)
        with self.assertRaisesRegex(ValidationError, 'Phone \+180055555 is not valid'):
            person = Person(
                'Test', 'Person', 'Test address',
                '+180055555', 'test@example.com')
        self.assertEqual(len(self.ab._book), 0)

    def test_create_person_fail_email(self):
        self.assertEqual(len(self.ab._book), 0)
        with self.assertRaisesRegex(ValidationError, 
                'Email testexample.com is not valid'):
            person = Person(
                'Test', 'Person', 'Test address',
                '+18005555555', 'testexample.com')
        self.assertEqual(len(self.ab._book), 0)

    def test_person_full_name(self):
        self.assertEqual(self.person.full_name, 'Test Person')

    def test_person_string(self):
        self.assertEqual(self.person.__str__(), 
                'Test Person (+18005555555) Test address test@example.com')

    def test_ab_add_person_fail(self):
        with self.assertRaises(AssertionError):
            self.ab.add('Wrong type')

    def test_ab_add_group(self):
        self.assertEqual(len(self.ab._groups), 0)
        self.ab.add(self.group)
        self.assertEqual(len(self.ab._groups), 1)

    def test_ab_search(self):
        self.ab.add(self.person)
        person = Person(
                'Test', 'Second', 'Test address',
                '+18005555555', 'noway@example.com')
        self.ab.add(person)
        result = self.ab.search('test')
        self.assertEqual(len(result), 2)
        result = self.ab.search('noway@example.com')
        self.assertEqual(len(result), 1)
        result = self.ab.search('noway')
        self.assertEqual(len(result), 1)
        result = self.ab.search('nothing')
        self.assertEqual(len(result), 0)

    def test_add_person_to_group(self):
        self.assertFalse(self.person.is_member_of('Test group'))
        self.group.add_person(self.person)
        self.assertTrue(self.person.is_member_of('Test group'))

    def test_remove_person_from_group(self):
        self.assertFalse(self.person.is_member_of('Test group'))
        self.group.add_person(self.person)
        self.assertTrue(self.person.is_member_of('Test group'))
        self.group.remove_person(self.person)
        self.assertFalse(self.person.is_member_of('Test group'))

    def test_get_group(self):
        self.ab.add(self.group)
        result = self.ab.get_group('Test group')
        self.assertEqual(len(result), 1)

    def test_tst_node_string(self):
        node = Node('a', key='b')
        self.assertEqual(node.__str__(), "Node: a {'b'}")

    def test_tst_in_tree(self):
        tree = self.ab._tst
        self.ab.add(self.person)
        self.assertTrue(tree.in_tree('test'))
        self.assertFalse(tree.in_tree('nothing'))

    def test_tst_traverse(self):
        tree = self.ab._tst
        self.ab.add(self.person)
        result = tree.traverse()
        self.assertSequenceEqual(result, [
            'p', 'e', 'r', 's', 'o', 'n',
            't', 'e', 's', 't', 
            't', 'e', 's', 't', 
            'e', 'x', 'a', 'm', 'p', 'l', 'e', '.', 'c', 'o', 'm',
            't', 'e', 's', 't', 'p', 'e', 'r', 's', 'o', 'n'])



if __name__ == '__main__':
    unittest.main()
