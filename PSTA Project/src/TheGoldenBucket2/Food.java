package TheGoldenBucket2;

public class Food extends Catalogue {

    Food(String name, double price) {
        super(name,price);
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
