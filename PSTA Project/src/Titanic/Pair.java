package Titanic;

public class Pair<K>{
    private K key;
    private Integer value;

    public Pair (K key, Integer value){
        this.key = key;
        this.value = value;
    }

    public void setValue (Integer value){
        this.value = value;
    }

    public K getKey () {return key;}

    public Integer getValue () {return value;}

    public String toString () {return "Key: " + key.toString() + ", Value: " + value.toString();}

    public Integer compareTo (Pair p){
        return value.compareTo(p.value);
    }
}
