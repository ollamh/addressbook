#!/usr/bin/python
class Node:
    """
    Ternary search tree node class.
    """
    
    def __init__(self, data=None, key=None):
        self.keys = set([])
        if key:
            self.keys.add(key)
        self.data = data
        self.right = None
        self.left = None
        self.eq = None

    def __str__(self):
        return 'Node: {} {}'.format(self.data, self.keys)


class TST:
    """
    Ternary search tree implementation. 
    Not the best one definitely.
    Good sides:
     - suits best for prefix searches
    Bad sides:
     - consumes lots of space
    """

    def __init__(self):
        self.root = Node()
        self.leaf = None

    @staticmethod
    def _search(node, child):
        while node:
            if node.data == child:
                return node
            if node.data is None or child > node.data:
                node = node.right
            else:
                node = node.left
        return None

    def _insert(self, node, child):
        if node is None:
            return child
        elif node.data is None or child.data > node.data:
            node.right = self._insert(node.right, child)
        elif child.data == node.data:
            return node
        else:
            node.left = self._insert(node.left, child)
        return node

    def insert(self, string, key=None):
        """
        Inserts string into tree.
        Key parameter is used to add key related to
        certain node, e.g. when inserting string
        'joe' -> 'j', 'o', 'e' will have key associated
        with 'joe'
        """
        node = self.root
        for char in string:
            child = self._search(node.eq, char)
            if not child:
                child = Node(char, key)
                node.eq = self._insert(node.eq, child)
            node = child
            if key:
                node.keys.add(key)
        if not self._search(node.eq, self.leaf):
            node.eq = self._insert(node.eq, Node(self.leaf))

    def in_tree(self, string):
        """
        Checks if string exists in the tree
        """
        node = self.root
        for char in string:
            node = self._search(node.eq, char)
            if not node:
                return False
        return self._search(node.eq, self.leaf) is not None

    def get(self, string):
        """
        Gets keys associated with current node
        """
        node = self.root
        for char in string:
            node = self._search(node.eq, char)
            if not node:
                return None
        return node.keys

    def _traverse(self, node, leaf):
        if node:
            for c in self._traverse(node.left, leaf):
                yield c
            if node.data == leaf:
                yield []
            else:
                for c in self._traverse(node.eq, leaf):
                    yield [node.data] + c
            for c in self._traverse(node.right, leaf):
                yield c

    def traverse(self):
        """
        Traverses tree (inorder traversal)
        """
        buff = []
        for c in self._traverse(self.root.eq, self.leaf):
            buff += c
        return buff
    
