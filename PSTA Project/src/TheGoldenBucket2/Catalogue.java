package TheGoldenBucket2;

public class Catalogue {
	public String name;
    public double price;

    public Catalogue(String name, double price) {
        this.name = name;
        this.price = price;
    }

    public String getName() {
    	return this.name;
    }
    
    public double getPrice() {
    	return this.price;
    }
    
    @Override
    public String toString() {
    	String descr = "Name: "+ name + "    |    " + "Price: " + price;
    	return descr;
    }
}
