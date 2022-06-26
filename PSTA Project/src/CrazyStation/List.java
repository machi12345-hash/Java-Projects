package CrazyStation;

public interface List<T> {
    void insert(T data);
    void printAll();
    int size();
    T popNode();
    boolean contains(T data);
    T getNode(int index);

    void deleteAt(int index);
}
