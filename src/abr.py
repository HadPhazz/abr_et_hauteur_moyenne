#!/usr/bin/python3
# -*- coding: utf-8 -*-
from binary_tree import BinaryTree
from binary_tree import BinaryTreeError

class AbrError(BinaryTreeError):
    def __init__(self, msg):
        super().__init__( msg)

class Abr(BinaryTree):
    """
    Arbre binaire de recherche

    :Exemples:

    >>> a = Abr()
    >>> a = a.insere(2) 
    >>> a = a.insere(3)
    >>> a == Abr(2, Abr(), Abr(3, Abr(), Abr()))
    True
    >>> a.recherche(4)
    False
    >>> a.recherche(3)
    True
    >>> a.maximum() == 3
    True
    >>> a = a.supprime(3)
    >>> a == Abr(2, Abr(), Abr())
    True
    """
    def __init__(self, *args):
        super().__init__(*args)
        if len(args) > 0:
            rac, sag, sad = args
            if not isinstance(sag, Abr) or not isinstance(sad, Abr):
                raise AbrError('type non conforme')
            if not sag.est_abr() or not sad.est_abr():
                raise AbrError('données non conformes')
        
    def ordre_infixe(self):
        return (self.get_left_subtree().ordre_infixe() + 
                [self.get_data()] + 
                self.get_right_subtree().ordre_infixe())
    
    def est_abr(self):
        #liste_infixe = ordre_infixe()
        #return all(liste_infixe[i] <= liste_infixe[i+1] for i in range(len(liste_infixe) - 1))
        if self.is_empty():
            return True
        else:
            return (self.get_left_subtree().est_abr() and
                    self.get_right_subtree().est_abr() and
                    (self.get_left_subtree().is_empty() or self.get_left_subtree().maximum() <= self.get_data()) and
                    (self.get_right_subtree().is_empty() or self.get_right_subtree().minimum() >= self.get_data()))
    
    def insere(self, elt):
        if self.is_empty():
            return Abr(elt, Abr(), Abr())
        elif elt <= self.get_data():
            return Abr(self.get_data(), self.get_left_subtree().insere(elt), self.get_right_subtree())
        elif elt > self.get_data():
            return Abr(self.get_data(), self.get_left_subtree(), self.get_right_subtree().insere(elt))
    
    def recherche(self, elt):
        if self.is_empty():
            return False
        elif elt == self.get_data():
            return True
        elif elt <= self.get_data():
            return self.get_left_subtree().recherche(elt)
        else:
            return self.get_right_subtree().recherche(elt)
    
    def minimum(self):
        sag = self.get_left_subtree()
        if sag.is_empty():
            return self.get_data()
        else:
            return sag.minimum()
    
    def maximum(self):
        sad = self.get_right_subtree()
        if sad.is_empty():
            return self.get_data()
        else:
            return sad.maximum()
        
    def supprime(self, elt):
        if self.is_empty():
            return Abr()
        else:
            if elt < self.get_data():
                return Abr(self.get_data(), self.get_left_subtree().supprime(elt), self.get_right_subtree())
            elif elt > self.get_data():
                return Abr(self.get_data(), self.get_left_subtree(), self.get_right_subtree().supprime(elt))
            else: # elt == rac
                if self.get_left_subtree().is_empty():
                    return self.get_right_subtree()
                else:
                    elt_max = self.get_left_subtree().maximum()
                    return Abr(elt_max, self.get_left_subtree().supprime(elt_max), self.get_right_subtree())
    
    def hauteur(self):
        if self.is_empty():
            return 0
        else:
            left_depth = self.get_left_subtree().hauteur() if self.get_left_subtree() else 0
            right_depth = self.get_right_subtree().hauteur() if self.get_right_subtree() else 0
            return max(left_depth, right_depth) + 1
