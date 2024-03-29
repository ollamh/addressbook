# Another one Address Book

This is an implementation of a address book, where you can do PREFIX search on
person by it's first name, last name or email. A Person has one or more emails,
street addresses, phone numbers, can be a part of a group. Then, you can find
by given group, it's members or by given Person, you can find his groups list.

The address book is using pickle module to store data. You can define file path
on initialization for address book to work with certain dataset, e.g.

    ab_work = AddressBook('work.dat') #  Will use a work address book
    ab_home = AddressBook('home.dat') #  Will use a personal address book

By defaul, address file name is 'addressbook.dat'.

For prefix search I'm using one of Tries implementation - a ternary search tree.
I adopted it for this particular solution, every node holds a set of keys which
point to corresponding persons data. Might be not a perfect solution but I
always wanted to work with it. Complexity for insertion, lookup in average is 
O(log n). Groups I store as a list, Persons I store in dictionary, with full name
as a key (it was the quickest solution, not the perfect one)

# Usage example

Initialization

    >>> from addressbook import AddressBook, Person
    >>> ab = AddressBook()

Add a person to the address book.

    >>> ab.add(Person('Jack', 'Jones', '234, 3rd avenue, City, Country', 
    ...    '+15555555555', 'jack.jones@example.com'))

Add a group to the address book.

    >>> ab.add(Group('Simple group'))
    
Given a group we want to easily find its members.

    >>> group = ab.get_group('Simple group')
    >>> print(group._persons)

Given a person we want to easily find the groups the person belongs to.

    >>> person = Person(..)
    >>> person.is_member_of(group)
    True or False

Find person by name (can supply either first name, last name, or both).
    
    >>> persons = ab.search('Jack')
    >>> print(persons)
    [<Jack Jones (+15555555555) 234, 3rd avenue, City, Country jack.jones@example.com>]

Find person by email address (can supply either the exact string or a prefix string, ie. both "alexander@company.com" and "alex" should work).
    
    >>> persons = ab.search('jack.jones@example.com') 
    >>> print(persons)
    [<Jack Jones (+15555555555) 234, 3rd avenue, City, Country jack.jones@example.com>]

Add address, email, phone number
    
    >>> jack = persons[0]
    >>> jack.add_address('444, A nice road, Home sweet home')
    >>> print(jack.addresses)
    ['234, 3rd avenue, City, Country', '444, A nice road, Home sweet home']
    
    >>> jack.add_phone('+18005555556')
    >>> print(jack.phones)
    ['+18005555555', '+18005555556']
    
    >>> jack.add_email('jack.another@mail.com')
    >>> print(jack.emails)
    ['jack.jones@example.com', 'jack.another@mail.com']
    
    
    
    
# API

## Person

### Parameters (all required):

        - first_name (string)
        - last_name (string)
        - street address (string)
        - phone number (string, starts with + or 00 following 10 numbers)
        - email (email-like string)

    person = Person('Jack', 'Jones', '234, 3rd avenue, City, Country', 
        '+15555555555', 'jack.jones@example.com')
    
### Attributes:

        full_name - returns first name and last name concatenated
        emails - list of person's emails
        addresses - list of person's addresses
        phones - list of person's phones
        groups - list of person's groups        

### Methods:

        add_address(address) - adds an address to person addresses

        # Will raise ValidationError if phone number is not starting with + or 00 followed by 10 numbers
        add_phone(phone_number) - adds phone number to person phones.
        
        # Will raise ValidationError if email is not a valid one        
        add_email(email) - adds email to person emails
        
        is_member_of(group_name) - checks if person is member of group. Return either True or False
        
        add_group(group) - adds group to person's groups list
        remove_group(group) - removes group from person's groups list
        

## Group

### Parameters (required):

        - name (string)

### Methods:
        
        add_person(person) - adds Person to Group
        remove_person(person) - removes Person from Group
        is_member_of(person_name) - checks if person is member of a Group

## AddressBook

### Parameters:
    
        - storage_file (string, non-required, default:'addressbook.dat') - path to storage file

### Methods:

        add(Person|Group) - adds Person or Group to AddressBook
        search(search_string) - performs prefix search on Person's first_name, last_name, full_name and email
        get_group(group_name) - gets Group by name        

# Design-only question

If to speak about finding a substring in any place of a string, among a set of
strings, we can use such algorithms as Boyer-Moore-Horspool or Knuth-Morris-Pratt
or a suffix tree (using Ukkonnen's algorithm for building a tree), which gives
us about a linear time complexity and possibility to say if the search string
is a substring of a emails set. 

We can keep records in a hash table, using email as a key (hoping that uniqueness
is a must) and lauch a search using map on keys, then, we'll have indexes of matches
in the keys list, and then we retrieve approppriate records.

Or we can store emails in suffix tree, together with key record information, so, by
finding substring we can get keys to access record.


# Setup environment for development

For the Debian
based linux, installation process will be:


     sudo apt-get install python-pip
     pip install virtualenv
     pip install virtualenvwrapper
     mkdir ~/.virtualenvs


Put inside your ~/.bashrc:
 
      if [ `which virtualenvwrapper.sh` ]; then 
        export WORKON_HOME=$HOME/.virtualenvs
        source `which virtualenvwrapper.sh`
        export PIP_RESPECT_VIRTUALENV=true
      fi

Then, create a projects environment:

    mkvirtualenv ginger --python=python3
    pip install -r requirements.txt  -- Only for tests
 
And every time you need to enable project environment, you need to
 run:
 
    workon ginger
 
After you finish with that:
 
    deactivate
 


# Run tests

To run tests you need to run in terminal:
  
    ./test.sh -v --with-coverage
    

