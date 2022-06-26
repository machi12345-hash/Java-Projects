package TheGoldenBucket2;

public class Main {

    public static void main(String[] args) {
    	
    	// OUR SWEET CUSTOMERS UWU
    	
    	Customer max = new Customer("Maxwell Powers");
    	
    	// EMPLOYEES
    	
    	Employee gordonRamsay = new Employee("Gordon Ramsey", "Kitchen Chef");
    	Employee peter = new Employee("Peter Griffin","Waiter");
    	Employee lois = new Employee("Lois Griffin","Cook");
    	Employee amirkia = new Employee("Amirkia Kia", "King of burgers");
    	Employee gabriel = new Employee("Gabriel Witte", "Bartender");
    	
    	// FOODS
    	
    	Food banana = new Food("Banana", 4.99);
    	Food potato = new Food("Potato", 2.9);
    	Food avocado = new Food("Avocado", 3.0);
    	Food magherita = new Food ("Pizza Magherita", 10.50);
    	Food antipasti = new Food ("Antipasti Selection", 9.70);
    	Food salami = new Food ("Pizza Salami", 11.30);
        
    	// DRINKS
    	
    	Drink cappucino = new Drink("Cappucino", 6.66);
    	Drink latte = new Drink("Latte", 2.49);
    	Drink coke = new Drink("Coca Cola", 4.2);
    	Drink cocktail  = new Drink ("Negroni Cocktail",8.70);
    
        LinkedListImpl<Drink> drinkList = new LinkedListImpl<Drink>();
        
        drinkList.insert(cappucino);
        drinkList.insert(latte);
        drinkList.insert(coke);
        
    	// ORDERS
    	
    	Order order1 = new Order(1);
    	Order order2 = new Order(2);
        
    	order1.addDrink(coke);
        order1.addFood(magherita);
        
        order2.addDrink(cocktail);
        order2.addFood(antipasti);
        order2.addFood(salami);
        
        // RESERVATIONS
        
        Reservation maxReservation = new Reservation(max,"8pm", "31.03.2022", peter);
        
        maxReservation.addOrder(order1);
        maxReservation.addOrder(order2);
        
        // IMPLEMENTATION
        
        System.out.println( "Dear Guest "+
                maxReservation.getCustomer().getName() +
                ", We thank you so much for your Business.\nTonight you had "+
                maxReservation.getOrders().size() +
                " Orders, which contain:\n ");
       
        maxReservation.printOrders();
        
        System.out.println("� Total Number of Drinks: " + maxReservation.calcTotalNumberOfDrinks());
        System.out.println("� Total Number of Foods: " + maxReservation.calcTotalNumberOfFoods());
        System.out.println("� Total Price: " + maxReservation.calcTotalPrice()+"�");
        System.out.println("� Your waiter was: "+maxReservation.getEmployee().getName());
    }
}

