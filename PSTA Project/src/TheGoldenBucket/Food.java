package TheGoldenBucket;

public class Food {

    // DATA

    private String name;
    private int price;

    // CONSTRUCTORS

    public Food(String name, int price) {
        this.name = name;
        this.price = price;
    }

    // METHODS

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }


    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }
}
