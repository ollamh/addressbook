#!/usr/bin/python
import collections
import pickle
import re

from addressbook.tst import TST

class ValidationError(Exception):
    pass

class Person:
    """
    Class defining a person
    """

    def __init__(self, first_name, last_name, address, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.addresses = []
        self.emails = []
        self.phones = []
        self.groups = []
        self.add_address(address)
        self.add_phone(phone)
        self.add_email(email)

    def add_address(self, address):
        self.addresses.append(address)

    def add_phone(self, phone):
        template = re.compile('^(?:\+|00)[\d\s\-\(\)]{10,}$')
        if template.match(phone):
            self.phones.append(phone)
        else:
            raise ValidationError('Phone {} is not valid'.format(phone))

    def add_email(self, email):
        template = re.compile(
                '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
        if template.match(email):
            self.emails.append(email)
        else:
            raise ValidationError('Email {} is not valid'.format(email))

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def __str__(self):
        return '{} ({}) {} {}'.format(
                self.full_name, self.phones[0],
                self.addresses[0], self.emails[0]
                )

    def is_member_of(self, group_name):
        result = filter(
                lambda group: group.name == group_name, 
                self.groups)
        try:
            next(result)
            return True
        except StopIteration:
            return False

    def add_group(self, group):
        if not group in self.groups:
            self.groups.append(group)

    def remove_group(self, group):
        if group in self.groups:
            self.groups.remove(group)
    

class Group:
    """
    Class representing groups of persons
    """

    def __init__(self, name):
        self.name = name
        self._persons = []

    def add_person(self, person):
        if not person in self._persons:
            self._persons.append(person)
        person.add_group(self)

    def remove_person(self, person):
        if person in self._persons:
            self._persons.remove(person)
        person.remove_group(self)

    def is_member_of(self, person_name):
        result = filter(
                lambda person: person.first_name == person_name or \
                person.last_name == person_name or \
                person.full_name == person_name or \
                person.email
                , 
                self._persons)
        try:
            next(result)
            return True
        except StopIteration:
            return False


class AddressBook:

    def __init__(self, storage_file=None):
        self.storage_file = storage_file or 'addressbook.dat'
        try:
            self._load_from_file()
        except:
            # TODO: Make as bucket list for same names-surnames
            self._book = collections.defaultdict(dict)  
            self._tst = TST()
            self._groups = []
            self._save_to_file()

    def _save_to_file(self):
        with open(self.storage_file, 'wb') as f:
            pickle.dump([self._book, self._tst, self._groups], f)

    def _load_from_file(self):
        with open(self.storage_file, 'rb') as f:
            self._book, self._tst, self._groups = pickle.load(f)


    def add(self, record):
        """
        Adds a person or a group to address book 
        """
        assert isinstance(record, (Person, Group)), \
            'Only Person or Group can be added to Address Book'
        if isinstance(record, Person):
            key = '{}{}'.format(record.first_name, record.last_name).lower()
            self._book[key] = record
            self._tst.insert(record.first_name.lower(), key)
            self._tst.insert(record.last_name.lower(), key)
            self._tst.insert(key, key)
            for email in record.emails:
                email = email.replace('@', '').lower()
                self._tst.insert(email, key)
        else:
            self._groups.append(record)
        self._save_to_file()

    def search(self, word):
        keys = self._tst.get(word.replace('@', '').replace(' ', '').lower())
        if keys:
            return [self._book[key] for key in keys]
        return []
        
    def get_group(self, group_name):
        """
        Return groups with certain name
        """
        return list(
                   filter(
                       lambda group: group.name == group_name, 
                       self._groups
                   )
               )

