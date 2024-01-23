import json
import random
import string
from typing import List

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key       : int,
                  word      : str,
                  leftchild,
                  rightchild):
        self.key        = key
        self.word      = word
        self.leftchild  = leftchild
        self.rightchild = rightchild

# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key": node.key,
            "word": node.word,
            "l": (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

# insert
# For the tree rooted at root, insert the given key,word pair and then balance as per AVL trees.
# The key is guaranteed to not be in the tree.
# Return the root.
def insert(root: Node, key: int, word: str) -> Node:
    # Fill in.
    if root is None:
        root = Node(key,word,None,None)
    elif key < root.key:
        root.leftchild = insert(root.leftchild, key,word)
    else:
        root.rightchild = insert(root.rightchild, key,word)
    
    balance = getBalance(root)
    if balance < -1: 
        if key < root.leftchild.key:
            return rotateRight(root)
        else:  
            root.leftchild = rotateLeft(root.leftchild)
            return rotateRight(root)
    elif balance > 1:
        if key > root.rightchild.key:  
            return rotateLeft(root)
        else:  
            root.rightchild = rotateRight(root.rightchild)
            return rotateLeft(root)
    return root

def getBalance(root: Node) -> int:
    if root is None:
        return 0
    return getHeight(root.rightchild) - getHeight(root.leftchild)

def rotateLeft(x:Node) -> Node:
    y = x.rightchild
    temp = y.leftchild
    y.leftchild = x
    x.rightchild = temp
    return y

def rotateRight(x:Node) -> Node:
    y = x.leftchild
    temp = y.rightchild
    y.rightchild = x
    x.leftchild = temp
    return y

def getHeight(node:Node) -> Node:
    if node is not None:
        leftHeight = getHeight(node.leftchild)
        rightHeight = getHeight(node.rightchild)
        return 1+ max(leftHeight, rightHeight)
    else:
        return -1



# bulkInsert
# The parameter items should be a list of pairs of the form [key,word] where key is an integer and word is a string.
# For the tree rooted at root, first insert all of the [key,word] pairs as if the tree were a standard BST, with no balancing.
# Then do a preorder traversal of the [key,word] pairs and use this traversal to build a new tree using AVL insertion.
# Return the root
def preorder(root: Node) -> str:
    def preorderAux(rootAux: Node, list: List[int]) -> List[int]:
        if rootAux:
            list.append(rootAux.key)
            preorderAux(rootAux.leftchild,list)
            preorderAux(rootAux.rightchild,list)
            return list
    preorderList = preorderAux(root, [])
    return(json.dumps(preorderList,indent =2))
def bulkInsert(root: Node, items: List) -> Node:
    # Fill in.
    def BSTInsert(rootNode: Node,key:int, word:str) -> Node:
        if rootNode is None:
            rootNode = Node(key,word,None,None)
        elif key < rootNode.key:
            rootNode.leftchild = BSTInsert(rootNode.leftchild, key,word)
        else:
            rootNode.rightchild = BSTInsert(rootNode.rightchild, key,word)
        return rootNode
    def preorderInsert(rootAux: Node, avlNode: Node) -> Node:
        if rootAux:
            avlNode = insert(avlNode,rootAux.key,rootAux.word)
            avlNode = preorderInsert(rootAux.leftchild,avlNode)
            avlNode = preorderInsert(rootAux.rightchild,avlNode)
        return avlNode
    
    for [key,word] in items:
        root = BSTInsert(root,int(key),word)
    avlNode = None
    avlNode = preorderInsert(root,avlNode)
    return avlNode #avlNode


# bulkDelete
# The parameter keys should be a list of keys.
# For the tree rooted at root, first tag all the corresponding nodes (however you like),
# Then do a preorder traversal of the [key,word] pairs, ignoring the tagged nodes,
# and use this traversal to build a new tree using AVL insertion.
# Return the root.
def bulkDelete(root: Node, keys: List[int]) -> Node:
    # Fill in.
    def tag(root: Node, key: int):
        if root:
            if root.key is key:
                root.word = 'xxxxxxxxxx'
            elif root.key > key:
                tag(root.rightchild,key)
            elif root.key < key:
                tag(root.leftchild,key)
    def preorderInsert(rootAux: Node, avlNode: Node, keyList:List[int]) -> Node:
        if rootAux:
            if (rootAux.word != 'xxxxxxxxxx' and rootAux.key not in keyList):
                avlNode = insert(avlNode,rootAux.key,rootAux.word)
            avlNode = preorderInsert(rootAux.leftchild,avlNode,keyList)
            avlNode = preorderInsert(rootAux.rightchild,avlNode,keyList)
        return avlNode
    for key in keys:
        tag(root,key) 
    avlNode = None
    avlNode = preorderInsert(root, avlNode,keys)  
    return avlNode

# search
# For the tree rooted at root, calculate the list of keys on the path from the root to the search_key,
# including the search key, and the word associated with the search_key.
# Return the json stringified list [key1,key2,...,keylast,word] with indent=2.
# If the search_key is not in the tree return a word of None.
def search(root: Node, search_key: int) -> str:
    # Fill in and tweak the resturn.
    def searchAux(rootAux: Node, key: int, list: List[int]) -> List[int]:
        if rootAux is not None:
            list.append(rootAux.key)
            if key == rootAux.key:
                list.append(rootAux.word)
                return list
            elif key > rootAux.key:
                return searchAux(rootAux.rightchild,key,list)
            elif key < rootAux.key:
                return searchAux(rootAux.leftchild, key,list)
        else:
            return list
    pathlist = searchAux(root, search_key,[])
    return json.dumps(pathlist,indent=2)
'''
def search(root: Node, search_key: int) -> str:
    # YOUR CODE GOES HERE.
    # Then tweak the next line so it uses your list rather than None.
    def searchAux(rootAux: Node, key: int, list: List[int]) -> List[int]:
        if rootAux is not None:
            list.append(rootAux.key)
            if key == rootAux.key:
                return list
            elif key > rootAux.key:
                return searchAux(rootAux.rightchild,key,list)
            elif key < rootAux.key:
                return searchAux(rootAux.leftchild, key,list)
        else:
            return list

    pathlist = searchAux(root, search_key,[])
    return(json.dumps(pathlist, indent = 2))'''
# replace
# For the tree rooted at root, replace the word corresponding to the key search_key by replacement_word.
# The search_key is guaranteed to be in the tree.
# Return the root
def replace(root: Node, search_key: int, replacement_word:str) -> None:
    # Fill in.
    if root:
        if search_key > root.key:
            replace(root.rightchild,search_key,replacement_word)
        elif search_key < root.key:
            replace(root.leftchild,search_key,replacement_word)
        else:
            root.word = replacement_word
    return root
'''
root1 = Node(50,'start',None,None)
insert(root1,60,'right1')
insert(root1,40,'left1')
insert(root1,45,'a')
insert(root1,47,'huhu')

print(dump(root1))'''


