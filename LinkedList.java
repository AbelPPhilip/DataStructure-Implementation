/*
 * @author Abelp
 * Name: Abel Philip
 * Date: 3/17/2022
 * Description: The Basic linked list
 */
package listClasses;

import java.util.*;


public class BasicLinkedList<T> implements Iterable<T> {
	
	/* Node definition */
	protected class Node {
		protected T data;
		protected Node next;

		protected Node(T data) {
			this.data = data;
			next = null;
		}
	}
	
	/* We have both head and tail */
	protected Node head, tail;
	
	/* size */
	protected int listSize;

	
	
	
	//constructor 
	public BasicLinkedList() {
		head = null;
		tail = null;
		listSize = 0;
	}
	//adds data to the end of the linked list
	public BasicLinkedList<T> addToEnd(T data){
		Node latest = new Node(data);
		if(head == null) {
			head = latest;
			tail = latest;
		}
		else {
			tail.next = latest;	
			tail = latest;
		}
		listSize++;
		return this;	
	}
	//adds data to front of linked list and updates the size
	public BasicLinkedList<T> addToFront(T data){
		Node latest = new Node(data);
		if (head == null) {
			head = latest;
			tail = latest;
		}
		else {
			latest.next = head;
			head = latest;
		}
		listSize++;
		return this;
	}
	
	//returns the first element 
	public T getFirst() {
		return (head == null ? null : head.data);
	}
	//returns the last element of the list
	public T getLast() {
		if(head == null) {
			return null;
		}
		Node curr = head; 
		while (curr.next != null) {
			curr = curr.next;
		}
		
		return curr.data;
	}
	//returns an arrayList of the reversed array 
	public ArrayList<T> getReverseArrayList(){
		ArrayList <T> list = new ArrayList <T> ();
		getReverseArrayList(head, list); 
		return list;
	}
	//private helper method
	private void getReverseArrayList(Node headAux, ArrayList<T>list){
		if (headAux!=null) {
			getReverseArrayList(headAux.next,list);
			list.add((T)headAux.data);
		}
	}
	//Returns a reversed linked list 
	public BasicLinkedList<T> getReverseList(){
		BasicLinkedList<T> reversed = new BasicLinkedList<T>();
		getReverseList(head, reversed);
		return reversed;
	}
	//private helper method
	private void getReverseList(Node headAux, BasicLinkedList<T> b) {
		if(headAux != null) {
			getReverseList(headAux.next,b);
			b.addToEnd(headAux.data);
		}
		
	}
	
	//Method removes target Data using the passed in comparator 
	public BasicLinkedList<T> remove(T targetData, Comparator<T> comparator){
		Node prev = null, curr = head;
		//this.comparator = comparator;
        
		while (curr != null) {
			if (comparator.compare(curr.data,targetData) == 0) {
				if (curr.equals(head)) {//if curr is head, current head will point to next
					head = head.next;
					prev = curr;
					curr = curr.next;
				} 
				else if (curr.equals(tail)){//if curr is tail, current tail will point to prev and next will be null 
					tail = prev;
					tail.next = null;
					prev = curr;
					curr = curr.next;
				}
				else {
					prev.next = curr.next;
					curr = curr.next;
				}
				listSize--;
			}else{
				prev = curr;
				curr = curr.next;
			}
		}
		return this;
	}
	//retrievees the first element and deletes the first element 
	public T retrieveFirstElement() {
		if(head==null) {//if list is empty
			return null;
		}
		else {
			T val = head.data;
			head = head.next;
			listSize--;
			return val;
		}
		
	}
	//Retrieves the last Element and delets the last element
	public T retrieveLastElement() {
		if(head == null) {//if list is empty
			return null;
		}
		else {
			Node prev = null, curr = head;
			while (curr!= null) {
				if (curr.equals(tail)){
					tail = prev;
					tail.next = null;
					listSize--;
					return curr.data;
				}
				prev = curr;
				curr = curr.next;
			}
			return null;
		}
		
	}
	//The iterator method that returns a iterator to use for each loops
	@Override
	public Iterator<T> iterator() {
		// TODO Auto-generated method stub
		return new Iterator<T>(){
			Node curr = head;

			public boolean hasNext() {
				return curr != null;
			}
			
			public T next() {
				T toReturn = curr.data;
				curr = curr.next;
				return toReturn; 
			}
		};
		
	}
    
	
	public int getSize() {
		return listSize;
	}
	//Returns head data 
	public T getHead() {
		return head.data;
	}
	//Return tail data 
	public T getTail() {
		return tail.data;
	}
	//Prints out the elements basic linked list 
	public String toString() {
		String result = "";
		Node curr = head;
		if (head == null) {
			return "";
		}
		else {
			while(curr != null) {
				result+= curr.data;
				if (curr.next!= null) {
					result += " ";
				}
				curr = curr.next;
			}
			return result;
		}
		
	}
}
