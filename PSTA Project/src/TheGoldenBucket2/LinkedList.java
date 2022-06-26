package TheGoldenBucket2;

import java.util.Iterator;

public interface LinkedList<T> extends Iterable<T>{

    void insert(T value);

    T retrieveAt(int index);

    int size();

    void remove();

    void show();

}