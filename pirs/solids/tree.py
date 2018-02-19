#!/bin/env python.my
# Copyright 2015 Karlsruhe Institute of Technology (KIT)
#
# This file is part of PIRS-2.
#
# PIRS-2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PIRS-2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
The Tree class defined in this module describes a tree. A tree consists of
nodes, which in turn are (sub)trees.

The term 'tree' will be used to refer to the tree as a whole, the term 'node'
will be used when local properties of a tree element (i.e. node) are discussed.

The terms 'parent' and 'child(ren)' denote hierarchical relation between tree
nodes. 'Direct parent of node C' is a node, where node C is inserted. The
direct node can be also inserted into another node, the latter is than
'indirect parent' of the node C. Similarly, 'direct child of node P' is a node,
which is inserted into P. Another node, inserted into the child node will be
denoted as 'indirect child' of P.

One parent node can have several child nodes. The order of child insertion is
saved.  The term 'sibling' denotes a node (nodes) inserted into the same
parent.  For example, A and B are inserted into node P. A and B are siblings.
"""

#at
# Author: Anton Travleev, anton.travleev@kit.edu
# Developed at INR, Karlsruhe Institute of Technology
#at
    

#### try:
####     from collections import OrderedDict
#### except ImportError:
####     try:
####         from ordereddict import OrderedDict
####     except ImportError as err:
####         print """
####         The hpmc package relies on collections.OrderedDict that is part of 
####         Python 2.7.
#### 
####         For earlier versions of Python, one needs to install manually the
####         package ordereddict from https://pypi.python.org/pypi/ordereddict/1.1. 
####         
#### 
####         Additional information can be found here:
####         http://stackoverflow.com/questions/1617078/ordereddict-for-older-versions-of-python
####         """
####         raise err

# OrderedDict = dict
# from copy import deepcopy
import random # to generate random tree for testing.
from .set_properties_as_kw import SetPropertiesAsKW

def do_indent(lines, indent_string=' '*8):
    """
    Returns a multi-line string whose lines are from argument lines indented with indent_string.
    
    >>> s = 'line 1\\n'
    >>> s+= 'line 2\\n'
    >>> s+= 'line 3'
    >>> print do_indent(s)
    line 1
            line 2
            line 3

    """
    r = lines.splitlines()
    r = ('\n' + indent_string).join(r)
    return r


class Tree(SetPropertiesAsKW):
    """
    Represents a tree hierarhical structure. 

    Originally, this class was written as a basis class for the classes in
    hpmc.solids, the latter represent solids (cylinder, box, sphere) inserted
    one into another.  For this reason, the common terminology for tree
    structures, like "parent" and "child", is mixed with a "geometry-inspired"
    terminology, e.g. "INSERT object n1 into object n2", or "withdraw object
    n3". The first example here, "INSERT n1 into n2" means to establish
    parent-child relation between objects n1 and n2, n1 being the parent and n2
    -- child.  The second example, "WITHDRAW n3" means to de-relate n3 with its parent (if any).

    When describing a tree hierarhical structure, one usually distinguishes
    between the tree as a whole, and elements (nodes) of the tree as tree
    constituing elements. Instances of the Tree class represent both concepts
    at the same time. It is a node. If this node has children, it is a tree.

    The constructor method takes no arguments,

    >>> t1 = Tree()
    >>> t2 = Tree()

    Any instance of the Tree class can have no or one parent and any number of children.

    The parent attribute references to the parent of the tree elementits
    parent (can be None) and '.children' attribute, which is an ordered
    dictionary of children (can be empty). To insert a node C into a node P, use
    method insert() of node P: 
    
    P.insert('key', C)
    C.parent            # is P
    P.children['key']   # is C

    Any child node has a key ('key' in the above example). This can be a string
    or integer (more exactly, any hashable type). The key is used to refer to
    children nodes.

    To withdraw C from P, use the method withdraw() of C:

    C.withdraw()

    Note, that insertion can be done only by the method of parent node, and
    withdrawal -- only by the method of child node.

    The insert() method returns the inserted node. In the code

    P = Tree()
    C = P.insert('key', Tree())

    P node instance is created first. Another node is created by calling Tree()
    and is inserted into P. This node instance can be referenced by C variable.

    A child node can be referenced by its key using the method get_child() of
    the parent node:

    P = Tree()
    C = Tree()
    P.insert('key', C)
    P.get_child('key')  # returns C

    Although direct access to the attributes '.parent' and '.children' is
    possible, do not set them directly, use methods insert() and withdraw()
    instead. Use these attributes only to get information, not to set. 

    Indirect children are referencesd by compound keys. A compound key is a
    TUPLE of keys (to distinguish compound keys and keys mentiond above in the
    insert() method, the latter are called 'local keys'). For example, C is
    inserted into P and A is inserted into C:

    P = Tree()
    C = Tree()
    A = Tree()
    P.insert('key C', C)
    C.insert('key A', A)

    Node A can than be referenced by the tuple ('key C', 'key A') from its
    indirect parent P. The compound keys can be given to the get_child()
    method:

    P.get_child( ('key C', 'key A') )  # returns A
    
    A zero-length compound key, (), references the element itself. A direct
    child with local key lkey can be referenced both with lkey and with
    compound key (lkey,).
    
    P.get_child( () )  # returns P
    P.get_child( 'key C' )  # returns C
    p.get_child(('key C'))  # returns C

    Local keys of siblings must be unique, i.e. there cannot be two direct
    children with the same local key (what happens if the allready used local
    key is used to insert another child node, see in the description of
    insert() method). However, child nodes inserted into different parents can
    have the same local key. In this case, their compound keys still differ.
    For example:

    P = Tree()
    A = P.insert(1, Tree())
    B = P.insert(2, Tree())
    C = A.insert(1, Tree())
    D = B.insert(1, Tree())

    Nodes C and D are inserted using the same local key, but they are inserted
    into different nodes.

    A child node can have only one parent (Reinsertion of already inserted node
    calls implicitly its withdraw() method first). Thus, any node can belong
    only to one tree. Method get_key() of a node returns the compound key of
    this node. For the above example,

    P.get_key()     # returns empty tuple, (,)
    A.get_key()     # returns (1,)
    C.get_key()     # returns (1, 1)
    D.get_key()     # returns (2, 1)

    A node not inserted into another one is called 'root node'. In the example
    above, this is node P.  The root node of a tree can be found by method
    get_root() of any another node of the tree.

    Methods keys(), items() and values() of a node return lists of all direct
    and indirect children of this node. For the differences see the description
    of these methods.

    Method get_parents() return a list of all parents (direct and indirect) of
    the node.  Method get_siblings() returns a tuple of two lists, which
    represent 'older' and 'younger' siblings of the node.

    There is possibility to change the order of inserted children. See method
    shift_child().

    Nodes can be copied. See methods copy_node() and copy_tree().

    """

    COPY_NODE_CALLS = 0
    COPY_TREE_CALLS = 0


    def __init__(self, **kwargs):
        self.__parent = None
        self.__children = [] 

        self.setp(**kwargs)

    @property
    def parent(self):
        """
        If self is inserted into another tree element, parent points to this element.
        """
        return self.__parent

    @property
    def local_index(self):
        """
        The position of element in its parent.
        """
        # explicit loop to use 'is' comparison, not '==' that is used implicitly by the 'in' operator.
        i = 0
        for c in self.__parent.__children:
            if c is self:
                return i
            i += 1
        raise IndexError('local index of child not found')

    @property
    def children(self):
        """
        An instance of the OrderedDict class where all children of self are stored.
        """
        return self.__children

    def parents(self, last=None):
        """
        Iterates over all parents of self, starting from the
        direct parent till the root.

        If optional argument last is given, iterates untill
        this parent, not untill the root.
        """
        if not last:
            last = self.root

        if self is not last and self.__parent:
            yield self.__parent
            for p in self.__parent.parents(last):
                yield p

    def withdraw(self):
        """
        Removes self from its parent. 

        Method returns self. 
        """
        if self.__parent != None:
            self.__parent.remove_child(self)
        return self    

    def remove(self, obj):
        """
        Removes child with local key lkey from the node. The removed element is
        returned.

        Note that this method provides functionality similar to the
        functionality of the withdraw method. The difference is that remove()
        removes child from self, and withdraw removes self from its parent.

        """
        if isinstance(obj, int):
            return self.remove_by_index(obj)
        else:
            return self.remove_child(obj)

    def remove_child(self, element):
        """
        Removes child from self.
        """
        li = element.local_index
        ch = self.__children[li]
        if ch is element:
            ch = self.__children.pop(li)
            ch.__parent = None
            return ch
        else:
            raise ValueError('Element not a child')

    def remove_by_index(self, i):
        """
        Removes i-th child.
        """
        ch = self.__children.pop(i)
        ch.__parent = None
        return ch

    def remove_by_criteria(self, **kwargs):
        """
        Removes direct shildren if they meet all criteria specified
        by kwargs. For example, 

        t.remove_by_criteria(name='fuel', i=3)

        will remove from t all children with name set to 'fuel' and
        positioned in the grid with i index equal to 3.

        Returns the list of removed elements.
        """

        # first loop to find elements to remove:
        toremove = []
        for i, e in enumerate(self.children):
            match = True
            for attr, value in kwargs.items():
                if getattr(e, attr) != value:
                    match = False
                    break
            if match:
                toremove.append(i)

        # second, remove the elements
        Nr = 0
        removed = []
        for i in toremove:
            removed.append( self.remove_by_index(i-Nr) )
            Nr += 1
        return removed





    def insert(self, othr, i=None):
        """
        Insert element ``othr`` into self.

        Optional argument ``i`` specifies index, where ``othr`` should be inserted. By
        default, ``othr`` is inserted as the last (most recent) child. One can specify
        ``i`` to set order fo the inserted element in the list of previously inserted.
        """
        cl = self.__children

        # If i is None, append othr to the end of children list.
        # If i is an integer, insert othr to the children's list to the position i,
        # so that the element having index i before insertion, gets index i+1 after
        # indertion.

        if i is None:
            othr.withdraw()
            self.__children.append(othr)
            othr.__parent = self
        else:
            othr.withdraw()
            self.__children.insert(i, othr)
            othr.__parent = self
        return othr

    def _append(self, othr):
        """
        Unconditinally inserts othr to the latest place.

        Assumes that othr is not previously inserted 
        """
        self.__children.append(othr)
        othr.__parent = self

    def shift_children(self, i, N, inew):
        """
        Shift children [i:i+N] to [inew:inew+N]
        """
        c = self.__children
        if inew < i:
            cnew = c[:inew] + c[i:i+N] + c[inew:i] + c[i+N:]
        elif i < inew:
            cnew = c[:i] + c[i+N:inew+N] + c[i:i+N] + c[inew+N:]
        else:
            cnew = c
        self.__children = cnew

    def id(self):
        """
        Returns id(self).
        """
        return id(self)

    def str_node(self, attr_=None):
        """
        Returns the string representing the node properties.

        The optional argument attr_ specifies the name of an attribute to print
        out. Can be a list of attribute names.

        >>> t = Tree()
        >>> t.str_node() == t.str_node('id()')    # by default, t.str_node() returns t.id()
        True
        >>> t.str_node('parent')                  # prints out the value of the parent attribute.
        "Tree 'parent': None"

        """

        s = self.__class__.__name__ 
        if attr_ == None:
            attr_ = ['id()']
        elif isinstance(attr_, list):
            # attr_.insert(0, 'id()')
            pass
        else:
            attr_ = [attr_]
        for a in attr_:
            try:
                s += ' ' + repr(a) + ': ' + str( eval('self.' + a) ) 
            except:
                s += ' ' + repr(a) + ': ----'
        return s

    def str_tree(self, attr_=None):
        """
        Returns a string representing the (sub)tree structure of the node and
        its children.

        The optional argument attr_ defines what will be printed. Its meaning
        and defualt see in the description of the str_node() method.

        >>> t = Tree()
        >>> t.inserT( 1, Tree())
        >>> t.inserT( 2, Tree())
        >>> t.get_child(1).inserT( 3, Tree())
        >>> t.inserT( 4, Tree())
        >>> print t.str_tree()                  #doctest: +ELLIPSIS
        Tree 'id()': ...
                - key 1: Tree 'id()': ...
                        - key 3: Tree 'id()': ...
                - key 2: Tree 'id()': ...
                - key 4: Tree 'id()': ...
        <BLANKLINE>
        """

        indentation = ' '*8
        s = self.str_node(attr_)
        s +='\n'
        for i, ch in enumerate(self.__children):
            s += indentation + '* {0}'.format(i)
            s += ': ' + do_indent( ch.str_tree(attr_), indentation ) 
            s += '\n'
        return s            

    def __str__(self):
        #return self.str_node()
        return self.str_tree()

    def keys(self):
        """
        Returns a list of compound keys of all children in self recursively.

        The order is depth-first.

        The local key specified in the insert() method refers only to the
        direct child. To refer to a node inserted into a child node, the
        compound key is used. The compound key is a tuple of local keys.

        >>> t = Tree()
        >>> t.inserT(1, Tree())
        >>> t.insert(2, Tree()).inserT(21, Tree())
        >>> t.insert(3, Tree()).insert(31, Tree()).inserT(311, Tree())
        >>> t.keys()
        [(1,), (2,), (2, 21), (3,), (3, 31), (3, 31, 311)]


        """
        for k, v in enumerate(self.__children):
            yield (k, )
            for kk in v.keys():
                yield (k, ) + kk

    def items(self, selfInclusive=False):
        """
        Returns a list of tuples (ckey, node) for all children in self
        recursively, where ckey is a compound key and node is the correspondent
        Tree instance.
        
        The order is depth-first.

        If the optional argument selfInclusive is True, the first element of
        the returned list is the node itself (by default, it is not included).
        
        >>> t = Tree()
        >>> t.inserT(1, Tree())
        >>> t.insert(2, Tree()).inserT(21, Tree())
        >>> t.items()         #doctest: +ELLIPSIS
        [((1,), <__main__.Tree object at ...>), ((2,), <__main__.Tree object at ...>), ((2, 21), <__main__.Tree object at ...>)]

        
        """
        if selfInclusive:
            yield ((self.local_index, ), self)
        for k, v in enumerate(self.__children):
            yield ((k, ), v)
            for kk in v.items():
                yield ((k, ) + kk[0], kk[1])

    def values(self, selfInclusive=False):
        """
        Returns a list of all children in self recursively.
        
        The order is depth-first.
        
        If the optional argument selfInclusive is True, the first element of
        the returned list is the node itself (by default, it is not included).

        >>> t = Tree()
        >>> t.inserT(1, Tree())
        >>> t.insert(2, Tree()).inserT(21, Tree())
        >>> t.values()         #doctest: +ELLIPSIS
        [<__main__.Tree object at ...>, <__main__.Tree object at ...>, <__main__.Tree object at ...>]

        """
        if selfInclusive:
            yield self
        for v in self.__children:
            yield v
            for kk in v.values():
                yield kk

    def get_child(self, k):
        """
        Returns the node with compound or local key k.

        The compound key is relative to the instance the method bound to.
        Compare with the result of get_key() method.

        If k is not a local key, can be indexed but has no 0-th element, the
        self is returned.  For example, if k is an empty tuple or an emtply
        string.

        
        """
        if isinstance(k, int):
            return self.__children[k]
        else:
            try:
                # can k be indexed?
                lkey = k[0]
                ckey = k[1:]
            except TypeError:
                # k cannot be indexed and not a local key. It cannot be a valid key.
                raise KeyError(k)
            except IndexError:
                # can be indexed, but k[0] does not exist. k is an empty tuple meaning th element self.
                return self
            return self.__children[lkey].get_child(ckey)

    @property
    def root(self):
        """
        Link to the root element of the tree self belongs to.
        """
        if self.__parent is None:
            return self
        else: return self.__parent.root

    def get_key(self):
        """
        Returns the compound key of the node relative to the tree root.
        
        >>> t = Tree()
        >>> t.insert(1, Tree()).inserT(2, Tree())
        >>> t.inserT(3, Tree())
        >>> for n in t.values():
        ...     print n.get_key()
        ...
        (1,)
        (1, 2)
        (3,)

        """
        if self.__parent is None:
            return tuple() 
        else:
            return self.__parent.get_key() + (self.local_index, )

    def get_parents(self, reverse=False):
        """
        Returns a  list of all node parents, starting from the direct parent and
        ending with the tree root.
        
        The optional boolean argument reverse changes the order of parents in
        the resulting list.

        >>> t = Tree()
        >>> t.insert(1, Tree()).inserT(2, Tree())
        >>> t.inserT(3, Tree())
        >>> for n in t.values():
        ...     print 'for ', n.get_key(), ' parents are: ', map(lambda x:x.get_key(), n.get_parents())
        ...
        for  (1,)  parents are:  [()]
        for  (1, 2)  parents are:  [(1,), ()]
        for  (3,)  parents are:  [()]
        
        
        """
        if self.__parent is None:
            return []
        else:
            pl = self.__parent.get_parents(reverse)
            if reverse: return pl + [self.__parent]
            else      : return [self.__parent] + pl

    def get_siblings(self):
        """
        Returns a tuple of two lists with nodes inserted into
        the node's parent before and after the node itself.

        For example, n0 contains 4 nodes:

        >>> n0 = Tree()
        >>> n1 = n0.insert(1, Tree())
        >>> n2 = n0.insert(2, Tree())
        >>> n3 = n0.insert(3, Tree())
        >>> n4 = n0.insert(4, Tree())

        >>> n2.get_siblings() == ([n1], [n3, n4])
        True
        >>> n1.get_siblings() == ([], [n2, n3, n4])
        True
        >>> n4.get_siblings() == ([n1, n2, n3], [])
        True

        """
        if self.__parent is None:
            return ([], [])

        y = [] # younger siblings
        o = [] #   older siblings
        found = False
        for c in self.__parent.__children:
            if c == self:
                found = True
            elif found:
                y.append(c)
            else:
                o.append(c)
        return (o, y)                

    def copy_tree(self):
        """
        Return a new instance containing copies of children (deep copy).
        """
        new = self.__class__()
        for v in self.__children:
            newv = v.copy_tree()

            new._append(v.local_key, newv)
        return new



    @classmethod
    def random_tree(cls, N=20, seed=None):
        """
        Returns a random tree with N nodes.

        Algorithm: untill the number of nodes in the tree, Ne, less than N,
        sample an integer from [1..Ne] and insert a new node as a child into
        the node with sampled number.
        
        Note, this is a class method.
        
        """
        r = cls() # tree to be returned
        l = [r]   # list representation of tree nodes.
        random.seed(seed)
        for i in range(N):
            n = random.randint(0, i)            # returns integer between 0 and i, which specifies the element where a new node will be inserted
            l.append( l[n].insert( cls() ) ) # create new node
        return r            


if __name__ == '__main__':
    import doctest
    doctest.testmod()

