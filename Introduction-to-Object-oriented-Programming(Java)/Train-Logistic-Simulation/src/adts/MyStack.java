package adts;

import java.util.ArrayList;

import intfs.StackIntf;

public class MyStack<T> implements StackIntf<T> {
	
	/**
	 * data added to the stack must be stored in <code>list</code>
	 */
	ArrayList<T> list = new ArrayList<T>();

	
	
	// CHANGES START BELOW THIS LINE
		
	/**
	 * {@inheritDoc}
	 */
	
	@Override
	public T push(T item) {
		list.add(item);
		return item;
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public T pop() {
		if(list!=null){
		T item = list.get(list.size()-1);
		list.remove(list.size()-1);
		return item;
		}
		else
			throw new NullPointerException();
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public T peek() {
		if(list!=null){
			return list.get(list.size()-1);
		}
		else
			throw new NullPointerException();
	}
	
	/**
	 * {@inheritDoc}
	 */
	@Override
	public boolean isEmpty() {
		
		return list==null;
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
