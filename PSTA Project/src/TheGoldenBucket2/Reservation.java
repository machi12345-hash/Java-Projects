package TheGoldenBucket2;

public class Reservation {
	
	// DATA
	
	private Customer c;
    private String time;
    private String date;
    private Employee waiter;
    private LinkedListImpl<Order> orderList;
    
    // CONSTRUCTORS
    
    Reservation (Customer c, String time, String date, Employee waiter){
        this.c = c;
        this.time = time;
        this.date = date;
        this.waiter = waiter;
        orderList = new LinkedListImpl<Order>();
    }
    
    // METHODS
    
    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getDate(){
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }
    public Employee getEmployee() {
        return waiter;
    }

    public void setEmployee(Employee waiter) {
        this.waiter = waiter;
    }

    public void addOrder(Order order) {
        orderList.insert(order);
    }

	
	public LinkedListImpl<Order> getOrders (){ 
		return orderList; 
	}
	 

    public Customer getCustomer (){
        return c;
    }
    
    public void printOrders() {
        for (int i = 0; i < orderList.size(); i++) {
        	System.out.println("\n----------------------- ORDER " + orderList.retrieveAt(i).orderId + "-----------------------");
        	orderList.retrieveAt(i).printDrinks();
        	orderList.retrieveAt(i).printFoods();
        }
        System.out.println("\n------------------------------------------------------");
    }
    
    public int calcTotalNumberOfDrinks() {
    	int counter = 0;
    	for (int i = 0; i < orderList.size(); i++) {
        	counter += orderList.retrieveAt(i).getDrinkNumber();
        }
    	return counter;
    }
    
    public int calcTotalNumberOfFoods() {
    	int counter = 0;
    	for (int i = 0; i < orderList.size(); i++) {
        	counter += orderList.retrieveAt(i).getFoodNumber();
        }
    	return counter;
    }
    
    public double calcTotalPrice() {
    	double total = 0;
    	for (int i = 0; i < orderList.size(); i++) {
    		for (int j = 0; j < orderList.retrieveAt(i).drinkList.size(); j++) {
            	total += orderList.retrieveAt(j).drinkList.retrieveAt(j).price; // implement getPrice
            }
    		for (int j = 0; j < orderList.retrieveAt(i).foodList.size(); j++) {
            	total += orderList.retrieveAt(j).foodList.retrieveAt(j).price; // implement getPrice
            }
        }
    	
    	return total;
    }
}
