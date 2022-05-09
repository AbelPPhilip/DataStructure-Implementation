package implementation;

import java.util.Comparator;
import java.util.TreeSet;


public class BinarySearchTree<K, V> {
	
	private class Node {
		private K key;
		private V value;
		private Node left, right;

		private Node(K key, V value) {
			this.key = key;
			this.value = value;
		}
	}

	private Node root;
	private int treeSize, maxEntries;
	private Comparator<K> comparator;

	public BinarySearchTree(Comparator<K> comparator, int maxEntries) {
		this.comparator = comparator; 
		this.maxEntries = maxEntries;
		treeSize = 0; 
	}

	public BinarySearchTree<K, V> add(K key, V value) throws TreeIsFullException {
		if (key == null || value == null) {
			throw new IllegalArgumentException("invalid Parameter");
		}
		if (root == null) {
			root = new Node(key, value);
			treeSize++;
			return this;
		} else {
			return addAux(key, value, root);
		}
	}
	private BinarySearchTree<K,V> addAux(K key, V value, Node rootAux) throws TreeIsFullException {
		if (!(this.isFull())) {
			int comparison = comparator.compare(key,rootAux.key);
			if (comparison == 0) {
				rootAux.value = value;
				return this;
			} else if (comparison < 0) {
				if (rootAux.left == null) {
					rootAux.left = new Node(key, value);
					treeSize++;
					return this;
				} else {
					return addAux(key, value, rootAux.left);
				}
			} else {
				if (rootAux.right == null) {
					rootAux.right = new Node(key, value);
					treeSize++;
					return this;
				} else {
					return addAux(key, value, rootAux.right);
				}
			}
		}
		else {
			throw new TreeIsFullException("Tree is full");
		}
	}

	public String toString() {
		return (this.isEmpty() ? "EMPTY TREE" : toStringAux(root));
	}

	private String toStringAux(Node rootAux) {
		return rootAux == null ? ""
				: toStringAux(rootAux.left) + "{" + rootAux.key + ":" + rootAux.value + "}" + toStringAux(rootAux.right);
	}

	/* Provided: n't modify */
	public boolean isEmpty() {
		return root == null;
	}

	/* Provided: n't modify */
	public int size() {
		return treeSize;
	}

	/* Provided: n't modify */
	public boolean isFull() {
		return treeSize == maxEntries;
	}

	public KeyValuePair<K, V> getMinimumKeyValue() throws TreeIsEmptyException {
		if (this.isEmpty()) {
			throw new TreeIsEmptyException("Tree is Empty");
		}
		else {
			Node min = getMinimumKeyValue(root);
			return new KeyValuePair<K,V> (min.key, min.value);
		}
	}
	 
	   
	
	private Node getMinimumKeyValue(Node rootAux){
		if  (rootAux.left == null) {
			return rootAux;
		}
		else {
			return getMinimumKeyValue(rootAux.left);
		}
		
	}

	public KeyValuePair<K, V> getMaximumKeyValue() throws TreeIsEmptyException {
		if (this.isEmpty()) {
			throw new TreeIsEmptyException("Tree is Empty");
		}
		else {
			Node max = getMaximumKeyValue(root);
			return new KeyValuePair<K,V> (max.key, max.value);
		}
	}
	
	private Node getMaximumKeyValue(Node rootAux) {
		if  (rootAux.right == null) {
			return rootAux;
		}
		else {
			return getMaximumKeyValue(rootAux.right);
		}
	}

	public KeyValuePair<K, V> find(K key) {
		return find(key, root);
	}

	private KeyValuePair<K,V> find(K key, Node rootAux) {
		if (rootAux == null) {
			return null;
		} else {
			int comparison = comparator.compare(key,rootAux.key);
			if (comparison == 0) {
				return new KeyValuePair<K,V>(rootAux.key, rootAux.value);
			} else if (comparison < 0) {
				return find(key, rootAux.left);
			} else {
				return find(key, rootAux.right);
			}
		}

	}
	

	public BinarySearchTree<K, V> delete(K key) throws TreeIsEmptyException {
		if (key == null) {
			throw new IllegalArgumentException("Invalid parameter");
		}
		if (this.isEmpty() || root == null) {
			throw new TreeIsEmptyException("Tree is empty");
		}
		root = delete(key,root);
		return this;
	}
	public Node delete(K key, Node rootAux){
		if (rootAux == null) {
			return null;
		}
		int comparison = comparator.compare(key, rootAux.key);
		if (comparison < 0) {
			rootAux.left = delete(key, rootAux.left);
		}
		else if ((comparison) > 0) {
			rootAux.right = delete(key, rootAux.right);
		}
	    else if (rootAux.left != null && rootAux.right != null) {
	    	rootAux.value = getMinimumKeyValue(rootAux.right).value;
	    	rootAux.right = retrieveMin(rootAux.right);
	    } 
	    else
	        rootAux = (rootAux.left != null) ? rootAux.left : rootAux.right;
	        return rootAux;
	}
	
	private Node retrieveMin(Node node){
		if (node.left != null) {
			node.left = retrieveMin(node.left);
			return node;
		} else
	        return node.right;
	}

	public void processInorder(Callback<K, V> callback) {
		inOrderTraversal(root,callback);
		
	}
	
	private void inOrderTraversal(Node rootAux,Callback<K, V> callback ) {
		if (rootAux.left != null) {
            inOrderTraversal(rootAux.left,callback);
		}
		callback.process(rootAux.key, rootAux.value);
		if (rootAux.right != null) {
			inOrderTraversal(rootAux.right,callback);
		}
	}

	public BinarySearchTree<K, V> subTree(K lowerLimit, K upperLimit) {
		BinarySearchTree<K,V>bst = new BinarySearchTree<K,V>(comparator,this.treeSize);	
		if (comparator.compare(root.key,lowerLimit)>0) {
			return subTree(lowerLimit, upperLimit, root.left,bst);
		}
		else if (comparator.compare(root.key, lowerLimit)<0) {
			return subTree(lowerLimit, upperLimit, root.right,bst);
		}
		else {
			return subTree(lowerLimit, upperLimit, root,bst);
		}
		
	}
	
	public BinarySearchTree<K,V> subTree(K low, K upper, Node rootAux, BinarySearchTree<K,V>bst){
		if (rootAux.left != null) {
            subTree(low,upper,rootAux.left,bst);
		}
		if (comparator.compare(rootAux.key, low)>=0 && comparator.compare(rootAux.key,upper)<=0) {
			subTreeAdd(rootAux,bst.root,bst);
		}
		if (rootAux.right != null) {
			subTree(low,upper,rootAux.right,bst);
		}
		return bst;
	}
	
	public BinarySearchTree<K,V> subTreeAdd(Node insertRoot,Node bstRoot,BinarySearchTree<K,V>bst){
		if (bst.root == null) {
			bst.root = new Node(insertRoot.key, insertRoot.value);
			return bst;
		}
		int comparison = comparator.compare(insertRoot.key,bstRoot.key);
		if (comparison == 0) {
			bstRoot.value = insertRoot.value;
			return this;
		} else if (comparison < 0) {
			if (bstRoot.left == null) {
				bstRoot.left = new Node(insertRoot.key, insertRoot.value);
				return bst;
			} else {
				return subTreeAdd(insertRoot, bstRoot.left,bst);
			}
		} else {
			if (bstRoot.right == null) {
				bstRoot.right = new Node(insertRoot.key,insertRoot.value);
				treeSize++;
				return this;
			} else {
				return subTreeAdd(insertRoot,bstRoot.right,bst);
			}
		}
	}
	

	public TreeSet<V> getLeavesValues() {
		TreeSet <V> values = new TreeSet<V>();
		return getLeavesValues(root, values);
	}
	
	public TreeSet<V> getLeavesValues(Node rootAux, TreeSet<V> tree){
		if (rootAux.left != null) {
			getLeavesValues(rootAux.left, tree);
		}
		if (rootAux.left == null && rootAux.right == null) {
			tree.add(rootAux.value);
		}
	    if (rootAux.right != null) {
	    	getLeavesValues(rootAux.right, tree);   
		}
	    return tree;
	    
	}
}
