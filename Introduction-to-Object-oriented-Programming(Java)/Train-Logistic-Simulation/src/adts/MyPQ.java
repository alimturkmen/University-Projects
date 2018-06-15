package adts;

import intfs.PriorityQueueIntf;

import java.util.LinkedList;

public class MyPQ<T extends Comparable<T>> implements PriorityQueueIntf<T> {


	/**
	 * data added to the stack must be stored in <code>list</code>
	 */
	LinkedList<T> list = new LinkedList<T>();

	// CHANGES START BELOW THIS LINE
	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean offer(T item) {
		if(list!=null){
		for(int i=0; i<list.size(); i++){
			T element = list.get(i);
			if(item.compareTo(element)==1){
				list.add(i, item);
				return true;
			}else if(item.compareTo(element)==0){
				list.add(i+1, item);
				return true;
			}
		}
			list.add(item);
			return true;
		}
		return false;
	}
	/**
	 * {@inheritDoc}
	 */
	@Override
	public T poll() {
		if(list!=null){
			T element = list.get(0);
			list.remove(0);
			return element;
		
		}
		return null;
	}
	/**
	 * {@inheritDoc}
	 */
	@Override
	public T peek() {
		if(list!=null)
			return list.get(0);
		return null;
	}
	/**
	 * {@inheritDoc}
	 */
	@Override
	public int count() {
		return list.size();
	}
	
	
	
	// CHANGES END ABOVE THIS LINE
	
}
