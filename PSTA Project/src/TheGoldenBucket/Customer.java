package TheGoldenBucket;

public class Customer {
    
    // DATA

    private String name; // Set to private for data encapsulation purposes

    // CONSTRUCTORS

    public Customer(String name) {
        this.name = name;
    }

    // METHODS

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
