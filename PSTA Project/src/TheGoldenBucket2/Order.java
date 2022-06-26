package TheGoldenBucket2;

public class Order {
	public int orderId;
	public Customer customer;
	public LinkedListImpl<Drink> drinkList;
	public LinkedListImpl<Food> foodList;
	
	public Order(int id){
        orderId = id; // maybe this should be given by linked list index? uWu
        drinkList = new LinkedListImpl<Drink>();
        foodList = new LinkedListImpl<Food>();
    }
	public int getFoodNumber () { 
		return foodList.size(); 
	}
	  
	public int getDrinkNumber () { 
		return drinkList.size(); 
	}
	  
	public void addFood (Food food) { 
		foodList.insert(food); 
	}
	  
	public void addDrink (Drink drink) { 
		drinkList.insert(drink); 
	}
	
	public void printFoods() {
		System.out.println("\nFOODS:");
        for (int i = 0; i < foodList.size(); i++) {
        	System.out.println("  � " +foodList.retrieveAt(i).name + "\t\t\t| " + foodList.retrieveAt(i).price+"�");
        }
    }
	
	public void printDrinks() {
		System.out.println("\nDRINKS:");
        for (int i = 0; i < drinkList.size(); i++) {
        	System.out.println("  � " +drinkList.retrieveAt(i).name + "\t\t\t| " + drinkList.retrieveAt(i).price+"�");
        }
    }
}
