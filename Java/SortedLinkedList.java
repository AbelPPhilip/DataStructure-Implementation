/*
 * @author Abelp
 * Name: Abel Philip
 * Date: 3/17/2022
 * Description: The sorted linked list
 */
package listClasses;

import java.util.*;


/**
 * Implements a generic sorted list using a provided Comparator. It extends
 * BasicLinkedList class.
 * 
 *  @author Dept of Computer Science, UMCP
 *  
 */

public class SortedLinkedList<T> extends BasicLinkedList<T> {
	Comparator <T> comparator;//comparator 
	//constructor with comparator parameter that calls super constructor. 
	public SortedLinkedList(Comparator <T> comparator){
		super();
		this.comparator = comparator; 
	}
	//Adds and an data element to the sorted linked list. 
	public SortedLinkedList<T> add(T element){
		Node curr = head, prev = null;
		Node latest = new Node(element);
		if(head == null) {
			head = latest;
			tail = latest;
			listSize++;
		}
		else {
			while(curr != null) {//loops through the linked list and inserts data. 
				if (comparator.compare(latest.data, curr.data)<=0) {//if given data is less than current data 
					if(curr == head) {//if the target is head, it shifts the head 
						latest.next = head;
						head = latest;
						listSize++;
						break;
					}
					else {//seperates node and inserts latest into the gap
						prev.next = latest;
						latest.next = curr;
						listSize++;
						break;
					}
				}
				else if (comparator.compare(latest.data, tail.data)>0) {//if given data is larger than tail, it updates tail
					tail.next = latest;
					tail = latest;
					listSize++;
					break;
				}
				else {//The iteration 
					prev = curr;
					curr = curr.next;
				}
			}
		}
		
		return this;
	}
	
	public SortedLinkedList<T> remove(T targetData){//remove method that calls the super method 
		return (SortedLinkedList<T>) super.remove(targetData, this.comparator);
	}
	
	@Override
	public BasicLinkedList<T> addToEnd(T data){//exception method that does not work
		throw new UnsupportedOperationException("Does not work");
	}
	
	@Override
	public BasicLinkedList<T> addToFront(T data){//exception method that does not work
		throw new UnsupportedOperationException("Does not work");
	}

}
