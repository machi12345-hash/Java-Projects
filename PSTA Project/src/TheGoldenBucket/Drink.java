package TheGoldenBucket;

public class Drink {

    // DATA

    private String name;
    private int price;

    // CONSTRUCTORS

    public Drink(String name, int price) {
        this.name = name;
        this.price = price;
    }
// METHODS


    public void setName(String name) {
        this.name = name;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }
}
