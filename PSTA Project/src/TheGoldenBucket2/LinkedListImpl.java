package TheGoldenBucket2;

import java.util.Iterator;
import java.util.NoSuchElementException;

public class LinkedListImpl<T> implements LinkedList<T>, Iterable<T>{

    Node<T> head;
    public int size;

    public void insert(T content) { // WORKS!
        Node node = new Node(content);
        Node copy = head;
        if (head == null) {
            head = node;
            size++;
        }
        else {
            while(copy.next != null) {
                copy = copy.next;
            }
            copy.next = node;
            size++;
        }
    }

   
   public void remove() { //works
        Node<T> temp = head;
        while (temp.next != null) {
            temp = temp.next;
        }

        temp = null;
        size--;
    }

    public void show() {
        Node<T> copy = head;
        if (head == null) {
            System.out.println("This bitch is empty! YEET!");
        }
        else {
            while(copy.next != null) {
                T item =  copy.obj;
                System.out.println(item.toString());
                copy = copy.next;
            }
        }
    }
    
    public T retrieveAt(int index) { // WORKS!
    	Node<T> copy = head;
    	int steps = 0;
    	while (steps != index) {
    		copy = copy.next;
    		steps += 1;
    	}
    		return  copy.obj;
    	}
    
    public int size() {
    	return this.size;
    }

    @Override
    public Iterator<T> iterator() {
        return new Iterator<T>() {

            Node<T> temp = head;


            @Override
            public boolean hasNext() {

                if (head == null) {
                    throw new NoSuchElementException();
                }
                if (temp.next != null) {
                    return true;
                }

                return false;
            }

            @Override
            public T next() {
                Node<T> returnElement = temp;

                temp = temp.next;

                return returnElement.obj;
            }
        };
    }
     class Node<T> {
        // DATA
        T obj;
        Node next;
        // CONSTRUCTORS
        Node(T obj) {
            this.obj = obj;
        }
    }

}
