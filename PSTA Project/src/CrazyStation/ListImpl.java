package CrazyStation;

public class ListImpl<T> implements List<T> {


    //helperclass for nodes
    static class Node<T> {

        T data;
        Node<T> next;

        Node(T data, Node next) {
            this.data = data;
            this.next = next;
        }

    }

    Node<T> head;

    //insert data at the end
    public void insert(T data) {

        Node<T> node = new Node<>(data, null);

        if (head == null) {
            head = node;
        }
        else {
            Node<T> n = head;

            while (n.next != null) {
                n = n.next;
            }
            n.next = node;
        }

    }

    //print all elements of list.
    public void printAll() {
        Node<T> n = head;
        if (n == null) {
            System.out.println("no wagons found");
            return;
        }
            while (n.next != null) {
                System.out.println(n.data.toString());
                n = n.next;
            }
            System.out.println(n.data.toString());

    }

    // counts the size of the list
    @Override
    public int size() {
        int counter = 1;
        Node<T> n = head;
        while (n.next != null) {
            counter++;
            n = n.next;
        }

        return counter;
    }

    //returns and removes first node
    @Override
    public T popNode() {

        Node<T> n = head;
        if(n == null) {

            return n.data;
        }else
        head = head.next;

        return  n.data;
    }

    //checks if data is in the list
    @Override
    public boolean contains(T data) {
        Node<T> n = head;
        while (n.next != null) {
            if (n.data.equals(data)) {
                return true;
            } else {
                n = n.next;
            }
        }
        return n.data.equals(data);
    }

    //returns a node bus leaves list unchanged
    @Override
    public T getNode(int index) {
        Node<T> n = head;
        int counter = 0;

        while (n.next != null) {
            if (counter == index) {
                break;
            } else {
                counter++;
                n = n.next;
            }
        }
        return  n.data;
    }

    //deletes a node from the list.
    @Override
    public void deleteAt(int index) {

        if (index == 0) {
            head = head.next;
        } else
        {
            Node n = head;
            Node n1 = null;

            for(int i=0;i<index-1;i++)
            {
                n = n.next;
            }
            n1 = n.next;
            n.next = n1.next;

        }
    }
}


