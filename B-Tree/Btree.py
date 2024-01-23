from __future__ import annotations
import json
from typing import List
import math

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  values   : List[str] = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.values   = values
        self.children = children
        self.parent   = parent

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = root

    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "keys": node.keys,
                "values": node.values,
                "children": [(_to_dict(child) if child is not None else None) for child in node.children]
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert.
    def insert(self, key: int, value: str):
        #checking if m < 2
        if self.m<2:
            return
        #if root is none
        if self.root is None:
            self.root = Node([key],[value],[None,None])
            return
        #find where to insert
        curr  = self.root 
        while curr.children and None not in curr.children:
            i = 0
            while i < len(curr.keys):
                if key < curr.keys[i]:
                    break
                i+=1
            curr = curr.children[i]
        
        #if curr is not full insert
        if len(curr.keys) < self.m -1:
            pos = 0
            while pos < len(curr.keys) and curr.keys[pos]<key:
                pos+=1
            curr.keys.insert(pos,key)
            curr.values.insert(pos,value)
            if None in curr.children:
                curr.children.append(None)
        else:
            #insert into curr (shove) 
            pos = 0 
            while pos < len(curr.keys) and curr.keys[pos]<key:
                pos+=1
            curr.keys.insert(pos,key)
            curr.values.insert(pos,value)
            if None in curr.children:
                curr.children.append(None)

            # if parent exists, not handling for now
            if self.rotate(curr):
                return
            
            parent = curr.parent
            medianIndex = (self.m-1)//2

            medianKey = curr.keys.pop(medianIndex)
            medianValue = curr.values.pop(medianIndex)
            leftKeys = curr.keys[:medianIndex]
            rightKeys = curr.keys[medianIndex:]
            leftChildren = []
            rightChildren = []
            
            leftNode = Node(keys = leftKeys,values = curr.values[:medianIndex],children = leftChildren)
            rightNode = Node(keys = rightKeys, values = curr.values[medianIndex:],children = rightChildren)

            if None in curr.children:
                for i in range(0,len(leftKeys)+1):
                    leftNode.children.append(None)
                for i in range(0,len(rightKeys)+1):
                    rightNode.children.append(None)
            else:
                leftNode.children = curr.children[:medianIndex+1]
                rightNode.children = curr.children[medianIndex+1:]
                for c in leftNode.children:
                    c.parent = leftNode
                for c in rightNode.children:
                    c.parent = rightNode
            
            if curr == self.root: #case of root
                self.root = Node(keys = [medianKey], values = [medianValue], children = [leftNode,rightNode])
                leftNode.parent = self.root
                rightNode.parent = self.root
                parent = self.root
            else:
                parent = curr.parent 
                parentIndex = parent.children.index(curr)
                
                parent.keys.insert(parentIndex,medianKey)
                parent.values.insert(parentIndex,medianValue)

                parent.children[parentIndex] = leftNode
                parent.children.insert(parentIndex+1,rightNode)

                leftNode.parent = parent
                rightNode.parent = parent
            
            
            if curr != self.root and len(parent.keys) == self.m:
                if self.rotate(parent):
                    return
                else:
                    self.split_node(parent)

    def split_node(self, curr: Node):
        medianIndex = (self.m-1)//2
        medianKey = curr.keys.pop(medianIndex)
        medianValue = curr.values.pop(medianIndex)
        leftKeys = curr.keys[:medianIndex]
        rightKeys = curr.keys[medianIndex:]
        leftChildren = []
        rightChildren = []
        leftNode = Node(keys = leftKeys,values = curr.values[:medianIndex],children = leftChildren)
        rightNode = Node(keys = rightKeys, values = curr.values[medianIndex:],children = rightChildren)
        #if curr has children
        if None in curr.children:
            for i in range(0,len(leftKeys)+1):
                leftNode.children.append(None)
            for i in range(0,len(rightKeys)+1):
                rightNode.children.append(None)
        else:
            leftNode.children = curr.children[:medianIndex+1]
            rightNode.children = curr.children[medianIndex+1:]
            for c in leftNode.children:
                c.parent = leftNode
            for c in rightNode.children:
                c.parent = rightNode

        if curr == self.root: #case of root
            self.root = Node(keys = [medianKey], values = [medianValue], children = [leftNode,rightNode])
            leftNode.parent = self.root
            rightNode.parent = self.root
        else:
            parent = curr.parent 
            parentIndex = parent.children.index(curr)
                
            parent.keys.insert(parentIndex,medianKey)
            parent.values.insert(parentIndex,medianValue)

            parent.children[parentIndex] = leftNode
            parent.children.insert(parentIndex+1,rightNode)

            leftNode.parent = parent
            rightNode.parent = parent 

            if len(parent.keys) >= self.m:
                if self.rotate(parent):
                    return
                else:
                    self.split_node(parent)

    def rotate(self, curr: Node) -> bool:
        parent = curr.parent
        if parent is None:
            return False
        parentIndex = parent.children.index(curr)
        
        # Check left sibling
        if parentIndex > 0:
            leftSib = parent.children[parentIndex-1]
            T = len(curr.keys) +len(leftSib.keys)
            targetSize = math.ceil(T/2)
            if len(leftSib.keys) < self.m-1:
                while len(curr.keys) > targetSize and len(leftSib.keys) < self.m-1:
                    #filling leftSib with key and values
                    leftSib.keys.append(parent.keys[parentIndex - 1])
                    leftSib.values.append(parent.values[parentIndex-1])
                    #moving the curr first key to parent
                    parent.keys[parentIndex -1] = curr.keys.pop(0)
                    parent.values[parentIndex - 1] = curr.values.pop(0)

                    #dealing with children
                    if curr.children and None not in curr.children:
                        child = curr.children.pop(0)
                    else:
                        curr.children.pop()
                        child = None

                    leftSib.children.append(child)
                    if child is not None:
                        child.parent = leftSib
                return len(curr.keys) <= targetSize
            
        if parentIndex <len(parent.children) -1 and len(curr.keys) > math.ceil(self.m/2)-1:
            rightSib = parent.children[parentIndex +1]
            T = len(curr.keys) +len(rightSib.keys)
            targetSize = math.ceil(T/2)
            if len(rightSib.keys) < self.m - 1:
                while len(curr.keys) > targetSize and len(rightSib.keys)<self.m-1:
                    #moving parent keys and value to right
                    rightSib.keys.insert(0,parent.keys[parentIndex])
                    rightSib.values.insert(0,parent.values[parentIndex])
                    #moving curr keys and values to parent
                    parent.keys[parentIndex] = curr.keys.pop()
                    parent.values[parentIndex] = curr.values.pop()
                    #dealing with children
                    if curr.children and None not in curr.children:
                        child = curr.children.pop()
                    else:
                        curr.children.pop()
                        child = None
                        
                    rightSib.children.insert(0,child)
                    if child is not None:
                        child.parent = rightSib

                return len(curr.keys) <= targetSize
        return False
        
    #DELETE
    def delete(self, key: int) -> Node:
        # Fill in the details.
        #if root is none 
        if self.root is None:
            return
        
        #finding the node with key
        curr  = self.root 
        while curr:
            i = 0
            while i < len(curr.keys) and key > curr.keys[i]:
                i+=1
            if i < len(curr.keys) and key == curr.keys[i]:
                #key is found and delete sequence is executed
                return self.deleteKey(curr,i)
            elif curr.children:
                curr = curr.children[i]
            else:
                curr = None
        #if key is not found
        if curr is None:
            return
    
    def deleteKey(self,curr: Node,index:int):
        #deleting the key
        #if the node is a leaf
        if None in curr.children:
            curr.children.pop()
            curr.keys.pop(index)
            curr.values.pop(index)    
            if len(curr.keys) >= math.ceil(self.m/2)-1 or (curr == self.root and len(curr.keys)>=1): #node has enough keys
                return
            else:
                self.rebalance(curr)
        else:#internal node
            #choosing successor
            successor = curr.children[index+1]
            while successor.children[0] is not None:
                successor = successor.children[0]
            successorKey, successorValue  = successor.keys[0], successor.values[0]
            curr.keys[index], curr.values[index] = successorKey, successorValue
            self.deleteKey(successor,0)
    
    def rebalance(self, curr:Node):
        if curr is None or curr == self.root:
            return
        
        parent = curr.parent
        parentIndex = parent.children.index(curr)
        underfullLimit = math.ceil(self.m/2)-1
        
        #add check for underfull if nessecary
        #right rotation from left sibling
        if (len(curr.keys)<underfullLimit):
            if parentIndex > 0:
                leftSib = parent.children[parentIndex - 1]
                T = len(curr.keys) + len(leftSib.keys)
                targetSize = math.floor(T/2)
                while len(curr.keys) < targetSize and len(leftSib.keys) > underfullLimit:
                    curr.keys.insert(0,parent.keys[parentIndex-1])
                    curr.values.insert(0, parent.values[parentIndex - 1])
                    parent.keys[parentIndex - 1] = leftSib.keys.pop()
                    parent.values[parentIndex - 1] = leftSib.values.pop()
                    # Adjust children if necessary
                    if leftSib.children and None not in leftSib.children:
                        child = leftSib.children.pop()
                    else:
                        leftSib.children.pop()
                        child = None
                    curr.children.insert(0,child)
                    if child is not None:
                        child.parent = curr
        if (len(curr.keys)<underfullLimit):
        #left rotation with right sibling
            if parentIndex < len(parent.children) - 1:
                rightSib = parent.children[parentIndex + 1]
                T = len(curr.keys) + len(rightSib.keys)
                targetSize = math.floor(T/2)
                while len(curr.keys) < targetSize and len(rightSib.keys) > underfullLimit:
                    # Move a key from right sibling to current node through the parent
                    curr.keys.append(parent.keys[parentIndex])
                    curr.values.append(parent.values[parentIndex])
                    parent.keys[parentIndex] = rightSib.keys.pop(0)
                    parent.values[parentIndex] = rightSib.values.pop(0)
                    # Adjust children if necessary
                    if rightSib.children and None not in rightSib.children:
                        child = rightSib.children.pop(0)
                    else:
                        rightSib.children.pop()
                        child = None
                    curr.children.append(child)
                    if child is not None:
                        child.parent = curr
        
        if len(curr.keys) < math.ceil(self.m/2)-1:
            self.merge(curr)
        
        if len(parent.keys) < math.ceil(self.m/2)-1 and parent != self.root:
            self.rebalance(parent)

    #merge function 
    def merge(self, curr: Node) -> None:
        parent = curr.parent
        if parent is None:
            return
        parentIndex = parent.children.index(curr)
        
        # Check left sibling
        if parentIndex > 0:
            leftSib = parent.children[parentIndex - 1]
            mergeKey = parent.keys.pop(parentIndex - 1)
            mergeValue = parent.values.pop(parentIndex - 1)
            parent.children.pop(parentIndex)
            # Update left sibling
            leftSib.keys.append(mergeKey)
            leftSib.values.append(mergeValue)
            leftSib.keys.extend(curr.keys)
            leftSib.values.extend(curr.values)
            if curr.children:
                leftSib.children.extend(curr.children)
                for child in curr.children:
                    if child is not None:
                        child.parent = leftSib
            if len(parent.keys) < math.ceil(self.m/2) -1:
                if parent == self.root:
                    if len(self.root.keys) == 0:
                        self.root.keys = leftSib.keys
                        self.root.values = leftSib.values
                        self.root.children = leftSib.children
            return
        # Check right sibling
        if parentIndex < len(parent.children) - 1:
            rightSib = parent.children[parentIndex + 1]
            # Update parent
            mergeKey = parent.keys.pop(parentIndex)
            mergeValue = parent.values.pop(parentIndex)

            parent.children.pop(parentIndex)

            # Update right sibling
            rightSib.keys.insert(0, mergeKey)
            rightSib.values.insert(0, mergeValue)
            rightSib.keys = curr.keys + rightSib.keys
            rightSib.values = curr.values + rightSib.values
            rightSib.parent = parent
            if curr.children:
                rightSib.children = curr.children + rightSib.children
                for child in curr.children:
                    if child is not None:
                        child.parent = rightSib
            if len(parent.keys) < math.ceil(self.m/2) -1:
                if parent == self.root:
                    if len(self.root.keys) == 0:
                        self.root.keys = rightSib.keys
                        self.root.values = rightSib.values
                        self.root.children = rightSib.children
            return 

    # Search
    def search(self,key) -> str:
        # Fill in and tweak the return.
        if self.root is None:
            return None
        path= []
        curr = self.root
        while curr:
            i = 0
            while i < len(curr.keys) and key > curr.keys[i]:
                i+=1
            if i < len(curr.keys) and key == curr.keys[i]:
                path.append('"{}"'.format(curr.values[i]))
                return '[{}]'.format(', '.join(path))
            if not curr.children:
                curr = None

            path.append(str(i))
            curr = curr.children[i]
        
        return None
