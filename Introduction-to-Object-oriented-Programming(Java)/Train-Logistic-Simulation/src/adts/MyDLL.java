package adts;

import intfs.DoublyLinkedListIntf;

public class MyDLL<T> implements DoublyLinkedListIntf<T>{

	/**
	 * Abstraction of a node in the Doubly Linked List (DLL) ADT.
	 *
	 * Example Usage: A Node in an integer DLL has the following fields:
	 * 		int data;
	 * 		Node<Integer> next, prev;
	 * 
	 * @param <E> type of the data.
	 */
	public class Node<E> {
		E data;
		Node<E> next;
		Node<E> prev;

		public Node(E data_) {
			data = data_;
		}
	}

	/**
	 *	The first node of the list.
	 *	NOTE: Made public for testing purposes.
	 */
	public Node<T> first;

	// CHANGES START BELOW THIS LINE
	
	/**
	 * {@inheritDoc}	
	 */
	
	@Override
	public void add(T item){
		if(first==null)
			first = new Node<T>(item);
		else{
			Node<T> newNode = first;
			while(newNode.next!=null)
				newNode = newNode.next;
			Node<T> newNode2 = new Node<T>(item);
			newNode.next = newNode2;
			newNode2.prev=newNode;
		
			
			
		}
	}
	/**
	 * {@inheritDoc}	
	 */
	
	@Override
	public boolean add(T item, int index){
		
		if(first==null)
			first=new Node<T>(item);
		Node<T> newNode = first;
		for(int i=0; i<index; i++){
			newNode=newNode.next;
		}
		if(newNode==null){
			newNode = new Node<T>(item);
			return true;
		}
		return false;
	}
	/**
	 * {@inheritDoc}	
	 */
	
	@Override
	public T remove(int index){
		if(index>=size() || index<0)
			throw new IndexOutOfBoundsException();
		Node<T> curr = first;
	    
	    for(int i=0; i < index; i++) {
	        curr = curr.next;
	        
	    }
	    T item=curr.data;
	    if(curr.prev==null && curr.next==null)
	    	first=null;
	    else if (curr.prev == null) {
	        curr.next.prev = null;
	        first = curr.next;
	    }else if(curr.next == null) {
	        curr = curr.prev;
	        curr.next = null;
	    }else{
	        curr.next.prev = curr.prev;
	        curr.prev.next = curr.next;
	    }  
	    return item;
    }  
	
	/**
	 * {@inheritDoc}	
	 */
	
	@Override
	public T get(int index){
		Node<T> newNode = first;
		for(int i=0; i<index; i++){
			newNode = newNode.next;
		}
		return newNode.data;
	}
	
	/**
	 *Returns the size of the doubly linked list.
	 *@return 
	 */
	public int size(){
		if(first==null)
			return 0;
		Node<T> newNode = first;
		int size=1;
		while(newNode.next!=null){
			newNode=newNode.next;
			size++;
		}
		return size;
	}
	
	

	// CHANGES END ABOVE THIS LINE

}
