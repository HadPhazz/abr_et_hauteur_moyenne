#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Éric Wegrzynowski'
__date_creation__ = 'Mon Oct 21 18:45:07 2019'
__doc__ = """
:mod:`binary_tree` module
:author: {:s} 
:creation date: {:s}
:last revision:

Define a class for binary trees.

Here is typical normal usage:

>>> t1 = BinaryTree()
>>> t1.is_empty()
True
>>> t2 = BinaryTree(1, t1, t1)
>>> t2.is_empty()
False
>>> t2.get_data()
1
>>> t2.get_left_subtree().is_empty()
True
>>> t2.get_right_subtree().is_empty()
True
>>> t2.is_leaf()
True
>>> print(t2)
(1, (), ())


and here are anormal usage

>>> t1.get_data()
Traceback (most recent call last):
  ...
BinaryTreeError: empty tree has no root
>>> t1.get_left_subtree()
Traceback (most recent call last):
  ...
BinaryTreeError: empty tree has no left subtree
>>> BinaryTree(1)
Traceback (most recent call last):
  ...
BinaryTreeError: bad arguments number for binary tree building
>>> BinaryTree(1, 2, 3)
Traceback (most recent call last):
  ...
BinaryTreeError: bad arguments type for binary tree building
""".format(__author__, __date_creation__)

import time
import graphviz

WHITE = '#FFFFFF'
BLACK = '#000000'

def escape_str(obj):
    '''
    convertit l'objet obj en une chaîne de caractères ASCII
    fct utile pour méthode to_dot des BinaryTree
    '''
    chaine = str(obj)
    chaine_echap = ''
    for c in chaine:
        n = ord(c)
        if 32 <= n <= 126 and c != '"':
            chaine_echap += c
        else:
            chaine_echap += '\\x{:04X}'.format(n)
    return chaine_echap
    
class BinaryTreeError(Exception):
    def __init__(self, msg):
        self.message = msg


class BinaryTree():
    def __init__(self, *args):
        """
        Binarytree Constructor

        :param args: any, BinaryTree , BinaryTree (optional) (Node, Left Child Tree, Right Child Tree )
        """
        if len(args) == 0:
            self._content = None
        elif len(args) != 3:
            raise BinaryTreeError('bad arguments number for binary tree building')
        elif not isinstance(args[1], BinaryTree) or not isinstance(args[2], BinaryTree):
            raise BinaryTreeError('bad arguments type for binary tree building')
        else:
            self._content = (args[0], args[1], args[2])

    @staticmethod
    def _is_atomic(expression):
        """
        :param expression: (str) a prefixed tree expression
        :return: (bool) True iff expression is atomic
        """
        return "," not in expression

    @staticmethod
    def _sub_expressions(expression):
        """
        :param expression: (str) an expression
        :return: (tuple) a tuple of len 3 (head, left expression, right expression)
        :CU: expression is a valid tree expression
        """
        res = []
        cpt = 0
        prev = 0
        i = 0
        while i < len(expression):
            if expression[i] == "(":
                cpt += 1
            if expression[i] == ")":
                cpt -= 1
            if expression[i] == "," and cpt == 0:
                res.append(expression[prev:i].strip("() "))
                prev = i+1
            i += 1
        res.append(expression[prev:i].strip("() "))
        return tuple(res)

    def unify(self, expression ):
        """
        :param expression: (str) an infix expression
        :return: (tuple) a couple (unified, subst) where
                - unified (bool) is True iff expression and tree are unified
                - subst (dict) te dictionary of substitutions

        >>> VIDE = BinaryTree()
        >>> BinaryTree(1, BinaryTree(2, VIDE, VIDE), BinaryTree(3, VIDE, VIDE)).unify("(a, b, c)")
        (True, {'a': 1, 'b': (2, (), ()), 'c': (3, (), ())})
        """
        res = True
        subst = {}
        if len(expression) > 0:
            if BinaryTree._is_atomic(expression):
                subst[expression] = self
            else:
                try:
                    data, left, right = BinaryTree._sub_expressions(expression.strip(")("))
                    subst[data.strip()] = self.get_data()
                    res_l, subst_l = self.get_left_subtree().unify(left)
                    res_r, subst_r = self.get_right_subtree().unify(right)
                    res = res_l and res_r
                    if res:
                        subst.update(subst_l)
                        subst.update(subst_r)
                except Exception as e:
                    res = False
                    print(e)
        return res, subst

    @staticmethod
    def from_prefix( prefix, substitutions ):
        """
        :param prefix: (str) a prefix expression
        :param substitutions: (dict) a dictionary associating key with BinaryTree
        :return: (BinaryTree) a new tree from prefix and substitutions
        """
        if BinaryTree._is_atomic(prefix):
            res = substitutions[ prefix ]
        else:
            d, left, right = BinaryTree._sub_expressions(prefix.strip("() "))
            assert d in substitutions, "{} n'est pas défini".format(d)
            res = BinaryTree( substitutions[d],
                              BinaryTree.from_prefix(left, substitutions),
                              BinaryTree.from_prefix(right, substitutions))
        return res

    def is_empty(self):
        """
        :return: (bool) True if this tree is empty
        """
        return self._content is None
        
    def get_data(self):
        """
        :return: (any) Value saved in the root node
        """
        try:
            return self._content[0]
        except TypeError:
            raise BinaryTreeError('empty tree has no root')

    def get_left_subtree(self):
        """
        :return: (BinaryTree) Left Child Subtree
        """
        try:
            return self._content[1]
        except TypeError:
            raise BinaryTreeError('empty tree has no left subtree')

    def get_right_subtree(self):
        """
        :return: (BinaryTree) Right Child subtree
        """
        try:
            return self._content[2]
        except TypeError:
            raise BinaryTreeError('empty tree has no right subtree')

    def size(self):
        """
        :return: (int) numbre of Nodes in Tree
        """
        if self.is_empty():
            return 0
        else:
            return 1 + self.get_left_subtree().size() + self.get_right_subtree().size()
        
    def height(self):
        """
        :return: (int) height of that tree
        """
        if self.is_empty():
            return -1
        else:
            return 1 + max(self.get_left_subtree().height(), self.get_right_subtree().height())

    def __eq__(self, obj):
        """
        :param obj: (any) an object
        :return: (bool) True iff obj is an instance of BinaryTree with same nodes in same order
        """
        if (isinstance(obj, BinaryTree)):
            if (self.is_empty()):
                res = obj.is_empty()
            else:
                rac = self.get_data()
                if not obj.is_empty():
                    res = ( rac == obj.get_data() and
                            self.get_left_subtree() == obj.get_left_subtree() and
                            self.get_right_subtree() == obj.get_right_subtree() )
                else:
                    res = False
        else:
            res = False
        return res
                
    def __str__(self):
        """
        :return: (str) string representation of that tree
        """
        if self.is_empty():
            return '()'
        else:
            repr_left = str(self.get_left_subtree())
            repr_right = str(self.get_right_subtree())
            return '({:s}, {:s}, {:s})'.format(str(self.get_data()), repr_left, repr_right)

    __repr__ = __str__
    
    def is_leaf(self):
        '''
        :return: (bool) True iff tree is a leaf
        '''
        return (not self.is_empty() and 
                self.get_left_subtree().is_empty() and
                self.get_right_subtree().is_empty())
    
    def to_dot(self, background_color=WHITE):
        '''
        :return: (str) dot representation of tree
        '''
        LIEN = '\t"N({:s})" -> "N({:s})" [color="{:s}", label="{:s}", fontsize="8"];\n'
        def aux(tree, prefix=''):
            if tree.is_empty():
                descr = '\t"N({:s})" [color="{:s}", label=""];\n'.format(prefix,
                                                                         background_color)
            else:
                c = tree.get_data()
                descr = '\t"N({:s})" [label="{:s}"];\n'.format(prefix, escape_str(c))
                s_a_g = tree.get_left_subtree()
                label_lien, couleur_lien = ('0', BLACK) if not s_a_g.is_empty() else ('', background_color)
                descr = (descr +
                         aux(s_a_g, prefix+'0') +
                         LIEN.format(prefix, prefix+'0', couleur_lien, label_lien))
                s_a_d = tree.get_right_subtree()
                label_lien, couleur_lien = ('1', BLACK) if not s_a_d.is_empty() else ('', background_color)
                descr = (descr +
                         aux(s_a_d, prefix+'1') +
                         LIEN.format(prefix, prefix+'1', couleur_lien, label_lien))

            return descr
    
        return '''/*
  Binary Tree

  Date: {}

*/

digraph G {{
\tbgcolor="{:s}";

{:s}
}}
'''.format(time.strftime('%c'), background_color, aux(self))       

    def _repr_png_(self):
        """
        """
        self.save('tree')
        return open('tree.png', 'rb').read()
    
    
    def show(self, filename='tree', background_color=WHITE):
        '''
        visualise l'tree et produit deux fichiers : filename et filename.png
        le premier contenant la description de l'tree au format dot, 
        le second contenant l'image au format PNG.
        '''
        descr = self.to_dot(background_color=background_color)
        graphviz.Source(descr, format='png').view(filename=filename)
    

    def save(self, filename='tree', background_color=WHITE):
        '''
        produit deux fichiers : filename et filename.png
        le premier contenant la description de l'tree au format dot, 
        le second contenant l'image au format PNG.
        '''
        graphviz.Source(self.to_dot(background_color=background_color), format='png').render(filename=filename)

if __name__ == '__main__':
   import doctest
   doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS, verbose=True)


