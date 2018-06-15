import java.util.ArrayList;

public class AVLTree<T extends Comparable<T>> implements AVLTreeInterface<T> {

	public Node<T> root;

	/**
	 * Basic storage units in a tree. Each Node object has a left and right
	 * children fields.
	 * 
	 * If a node does not have a left and/or right child, its right and/or left
	 * child is null.
	 * 
	 */
	private class Node<E> {
		private E data;
		private Node<E> left, right; // left and right subtrees

		public Node(E data) {
			this.data = data;
		}
	}

	// CHANGES START BELOW THIS LINE
	/**
	 * Stores the data of the nodes that visited by in order traversal.
	 */
	private ArrayList<T> inOrderList = new ArrayList<T>();
	/**
	 * Stores the data of the nodes that visited by breadth first traversal.
	 */
	private ArrayList<T> bfList = new ArrayList<T>();
	/**
	 * Stores the nodes of the tree.
	 */
	private ArrayList<Node<T>> nodes = new ArrayList<Node<T>>();
	/**
	 * The number of nodes in the tree
	 */
	private int size=0;
	
	@Override
	public boolean isEmpty() {
		
		return size()== 0 ? true : false;
	}

	@Override
	public int size() {
		return size;
	}

	@Override
	public boolean contains(T element) {
		
		Node<T> newNode = root;
		while(newNode!=null){
			if(element.compareTo(newNode.data)>0)
				newNode=newNode.right;
			else if(element.compareTo(newNode.data)<0)
				newNode=newNode.left;
			else
				return true;
		}
		return false;
			
	}
	
	@Override
	public void insert(T element) {
		
		if(!contains(element)){
		root=insert(element, root);
		size++;
		}
	}
	
	/**
	 * Inserts the element in the correct node. After insertion controls each node one by one using balanceFactor method
	 * By rotating balance the nodes again.
	 * @param element
	 * @param node
	 * @return
	 * @see balanceFactor
	 */
	public Node<T> insert(T element, Node<T> node){
		if(node==null)
			node = new Node<T>(element);	
		if(element.compareTo(node.data)<0){
			node.left = insert (element, node.left);
			if(balanceFactor(node.data)==2){
				if(element.compareTo(node.left.data)<0)
					node = rightRotation(node);
				else{
					node.left = leftRotation(node.left);
					node = rightRotation(node);
				}
			}
		}else if(element.compareTo(node.data)>0){
			node.right = insert (element, node.right);
			if(balanceFactor(node.data)==-2){
				if(element.compareTo(node.right.data)>0)
					node = leftRotation(node);
				else{
					node.right = rightRotation(node.right);
					node = leftRotation(node);
				}
			}
		}
		return node;
	}

	@Override
	public void delete(T element) {
		
		if(contains(element)){
		root=delete(root, element);
		size--;
		}
	}

	/**
	 * Deletes the given element from the tree and returns the node which takes place of the deleted node. 
	 * The successor node is the maximum node of the left subtree of the deleted node.
	 * After deleting process, controls for the balance by using balanceFactor method. 
	 * 
	 * @param node
	 * @param element
	 * @return
	 * @see balanceFactor
	 */
	public Node<T> delete(Node<T> node, T element) {
	    if (element.compareTo(node.data)<0) {
	        node.left = delete(node.left, element);
	    }else if (element.compareTo(node.data)>0) {
	        node.right = delete(node.right, element);
	    }else {
	        if ((node.left == null) || (node.right == null)) {
	            Node<T> tempNode = null;
	            if (tempNode == node.right) {
	                tempNode = node.left;
	            }else {
	                tempNode = node.right;
	            }
	            if (tempNode == null) {
	                tempNode = node;
	                node = null;
	            }else 	
	                node = tempNode;
	        }else{
	            Node<T> temp=maxNode(node.left);
	            node.data = temp.data;
	            node.left = delete(node.left, temp.data);
	        }
	    }
	    if (node == null) {
	        return node;
	    }
	    if(balanceFactor(node.data)==2){
	    	if (balanceFactor(node.left.data) >= 0) {
	            return rightRotation(node);
	        }else{
	            node.left = leftRotation(node.left);
	            return rightRotation(node);
	    	}
	    }
	    if(balanceFactor(node.data)==-2){
	        if (balanceFactor(node.right.data) <= 0) {
	            return leftRotation(node);
	    	}else{
	            node.right = rightRotation(node.right);
	            return leftRotation(node);	
	    	}
	    }
	    return node;
	}
	
	/**
	 * Finds and returns the maximum node of the subtree
	 * @param node
	 * @return
	 */
	public Node<T> maxNode(Node<T> node) {
	    Node<T> newNode = node;
	    while (newNode.right != null) 
	        newNode = newNode.right;
	    return newNode;
	}

	@Override
	public int height() {
		return height(root);
	}
	
	/**
	 * Returns the number of edges from the given node to the deepest leaf. 
	 * @param node
	 * @return
	 */
	public int height(Node<T> node){
		return node==null? -1 : 1+Math.max(height(node.left), height(node.right));
	}

	@Override
	public ArrayList<T> inOrderTraversal() {
		
		inOrderList.clear();
		inOrder(root);
		return inOrderList;
	}
	
	/**
	 * Visits each node of the tree, from leftmost one to rightmost one by using recursion.
	 * Stores the data in the each node that is visited, in the ArrayList.
	 * @param node
	 */
	public void inOrder(Node<T> node){
		
		if(node.left!=null){
			inOrder(node.left);
		}
		inOrderList.add(node.data);
		if(node.right!=null){
			inOrder(node.right);
		}
	}

	@Override
	public ArrayList<T> bfTraverse() {
		
		bfList.clear();
		breadthFirst(root);
		return bfList;
	}
	/**
	 * Starting from the given node, visits each level of the subtree.
	 * Adds each node to an ArrayList, from leftmost node to rightmost one in a level.
	 * Then by using another ArrayList, stores the data which is located inside the ArrayList of nodes.
	 * After taking the data from the node, removes the node from the ArrayList.
	 * @param node
	 */
	public void breadthFirst(Node<T> node){
		if(node==null)
			return;
		nodes.clear();
		nodes.add(root);
	    while(!nodes.isEmpty()){
	        Node<T> tempNode = nodes.get(0);
	        bfList.add(tempNode.data);
	        if(tempNode.left != null)
	        	nodes.add(tempNode.left);
	        if(tempNode.right != null) 
	        	nodes.add(tempNode.right);
	        nodes.remove(0);
	    }
	}
	
	@Override
	public boolean areCousins(T element1, T element2) {
		if(!contains(element1) || !contains(element2))
			return false;
		if(element1.compareTo(element2)==0)
			return false;
		Node<T> newNode = root;
		Node<T> newNode2 = root;
		int counter1=0;
		int counter2=0;
		while(newNode.data.compareTo(element1)!=0 || newNode2.data.compareTo(element2)!=0){
			if(element1.compareTo(newNode.data)>0){
				newNode = newNode.right;
				counter1 ++;
			}
			else if(element1.compareTo(newNode.data)<0){
				newNode = newNode.left;
				counter1 ++;
			}
			if(element2.compareTo(newNode2.data)>0){
				newNode2 = newNode2.right;
				counter2 ++;
			}
			else if(element2.compareTo(newNode2.data)<0){
				newNode2 = newNode2.left;
				counter2 ++;
			}	
		}
		if(sameParent(newNode, newNode2))
			return false;
		if(counter1==counter2)
			return true;
		else
			return false;
	}
	
	/**
	 * Checks whether the nodes that are sent have the same parent or not.
	 * If they have returns true, otherwise returns false.
	 * @param node1
	 * @param node2
	 * @return
	 */
	public boolean sameParent(Node<T> node1, Node<T> node2){
		Node<T> newNode = root;
		while(!equals(newNode.left,node1) && !equals(newNode.right,node1)){
			if(node1.data.compareTo(newNode.data)>0)
				newNode = newNode.right;
			else
				newNode = newNode.left;
		}
		if(equals(node2, newNode.left) || equals(node2, newNode.right))
		return true;
		return false;
		
	}
	
	/**
	 * If the received nodes are equal returns true, otherwise returns false.
	 * @param node1
	 * @param node2
	 * @return
	 */
	public boolean equals(Node<T> node1, Node<T> node2){
		return node1.data.compareTo(node2.data)==0 ? true : false;
	}
	@Override
	public int numElementsInRange(T lower, T upper) {
		int num=0;
		ArrayList<T> tempList = inOrderTraversal();
		for(int i=0; i<size(); i++){
			T element = tempList.get(i);
			if(element.compareTo(upper)<0 && element.compareTo(lower)>0)
				num++;
		}
		return num;
	}

	@Override
	public int balanceFactor(T data) {
		Node<T> newNode = root;
		while(newNode.data.compareTo(data)!=0){
			if(data.compareTo(newNode.data)<0)
				newNode = newNode.left;
			else if(data.compareTo(newNode.data)>0)
				newNode = newNode.right;
		}
		return (height(newNode.left)-height(newNode.right));
			
	}
	/**
	 * Rotates the tree right about the given node.
	 * Then returns the node which took the place of the given node.
	 * @param newNode
	 * @return
	 */
	public Node<T> rightRotation(Node<T> newNode){
		
		Node<T> leftright = newNode.left.right;
		Node<T> tempNode = newNode.left;
		tempNode.right = newNode;
		tempNode.right.left=leftright;
		return tempNode;
	}
	/**
	 * Rotates the tree left about the given node.
	 * Then returns the node which took the place of the given node.
	 * @param newNode
	 * @return
	 */
	public Node<T> leftRotation(Node<T> newNode){
		
		Node<T> rightleft = newNode.right.left;
		Node<T> tempNode = newNode.right;
		tempNode.left = newNode;
		tempNode.left.right=rightleft;
		return tempNode;
	}
	
	// CHANGES END ABOVE THIS LINE	
}
