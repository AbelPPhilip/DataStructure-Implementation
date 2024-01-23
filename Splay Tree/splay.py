from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  leftchild  = None,
                  rightchild = None,
                  parent     = None,):
        self.key        = key
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent

# DO NOT MODIFY!
class SplayTree():
    def  __init__(self,
                  root : Node = None):
        self.root = root

    # For the tree rooted at root:
    # Return the json.dumps of the object with indent=2.
    # DO NOT MODIFY!
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            pk = None
            if node.parent is not None:
                pk = node.parent.key
            return {
                "key": node.key,
                "left": (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "right": (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parentkey": pk
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Search
    def search(self,key:int):
        self.splay(key)
        

    # Insert Method 1

    #INSERT BST FOR TESTING PURPOSES
    def insertBST(self, key: int):
        if self.root:
            self._insert_recursive(self.root, key)
        else:
            self.root = Node(key)

    def _insert_recursive(self, current_node, key):
        if key < current_node.key:
            if current_node.leftchild is None:
                current_node.leftchild = Node(key, parent=current_node)
            else:
                self._insert_recursive(current_node.leftchild, key)
        else:
            if current_node.rightchild is None:
                current_node.rightchild = Node(key, parent=current_node)
            else:
                self._insert_recursive(current_node.rightchild, key)

    #___________________________________________________________________

    def insert(self,key:int):
        if self.root is None:
            self.root = Node(key,None,None,None)
            return
        self.splay(key)
        root = self.root
        if root.key == key:
            return

        newRoot = Node(key)
        if key < root.key:
            newRoot.rightchild = root
            newRoot.leftchild = root.leftchild
            if root.leftchild:
                root.leftchild.parent = newRoot
            root.leftchild = None
        else:
            newRoot.leftchild = root
            newRoot.rightchild = root.rightchild
            if root.rightchild:
                root.rightchild.parent = newRoot
            root.rightchild = None
        root.parent = newRoot
        self.root = newRoot
    
    def rotateLeft(self,x:Node):
        y = x.rightchild
        x.rightchild = y.leftchild  # Turn y's left subtree into x's right subtree
        if y.leftchild:
            y.leftchild.parent = x  # If y's left subtree exists, update its parent to x
        y.parent = x.parent  # Link y's parent to x's parent

        if x.parent is None:  # If x was the root,
            self.root = y  # make y the new root
        elif x == x.parent.leftchild:  # If x was a left child,
            x.parent.leftchild = y  # make y the left child of x's parent
        else:  # If x was a right child,
            x.parent.rightchild = y  # make y the right child of x's parent

        y.leftchild = x  # Make x the left child of y
        x.parent = y  # Update x's parent to y
        return y  # Return the new root of the subtree

        

    def rotateRight(self,x:Node):
        y = x.leftchild
        x.leftchild = y.rightchild  # Turn y's right subtree into x's left subtree
        if y.rightchild:
            y.rightchild.parent = x  # If y's right subtree exists, update its parent to x
        y.parent = x.parent  # Link y's parent to x's parent

        if x.parent is None:  # If x was the root,
            self.root = y  # make y the new root
        elif x == x.parent.leftchild:  # If x was a left child,
            x.parent.leftchild = y  # make y the left child of x's parent
        else:  # If x was a right child,
            x.parent.rightchild = y  # make y the right child of x's parent

        y.rightchild = x  # Make x the right child of y
        x.parent = y  # Update x's parent to y
        return y  # Return the new root of the subtree
        
    
    def findNode(self,key:int) -> Node:
        node = self.root
        last = self.root
        while node:
            last = node
            if key < node.key:
                node = node.leftchild
            elif key > node.key:
                node = node.rightchild
            else:
                return node
        return last
    def splay(self,key:int) -> None:
        x = self.findNode(key)
        while x.parent:
            if x.parent.parent is None: #Last Case when parent is the root and only one operation needed Zig
                if x == x.parent.leftchild: 
                    self.rotateRight(x.parent)
                else:
                    self.rotateLeft(x.parent)
            elif x == x.parent.leftchild and x.parent == x.parent.parent.leftchild: #Zig Zig   
                self.rotateRight(x.parent.parent)
                self.rotateRight(x.parent)
            elif x == x.parent.rightchild and x.parent == x.parent.parent.rightchild: #Zig Zig 
                self.rotateLeft(x.parent.parent)
                self.rotateLeft(x.parent)
            elif x == x.parent.rightchild and x.parent == x.parent.parent.leftchild: #Zig Zag
                self.rotateLeft(x.parent)
                self.rotateRight(x.parent)
            else:#Zig Zag
                self.rotateRight(x.parent) 
                self.rotateLeft(x.parent)
            if self.root == x:
                break
        self.root = x 

                   
    # Delete Method 1
    def delete(self,key:int):
        if self.root is None:
            return
        self.splay(key)
        if self.root.key != key:
            return
        
        if self.root.leftchild is None or self.root.rightchild is None:
            self.root = self.root.leftchild if self.root.leftchild else self.root.rightchild
            if self.root:
                self.root.parent = None
        else:
            rightSubtree = self.root.rightchild
            leftSubtree = self.root.leftchild
            #detaching the subtrees
            rightSubtree.parent = None
            leftSubtree.parent = None

            ios = rightSubtree
            while ios.leftchild:
                ios = ios.leftchild
            self.splay(ios.key)

            ios.leftchild = leftSubtree
            leftSubtree.parent = ios
            self.root = ios
        



