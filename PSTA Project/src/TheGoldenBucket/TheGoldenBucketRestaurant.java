package TheGoldenBucket;

public class TheGoldenBucketRestaurant {

    public static void main(String[] args) {

        // creating new reservation, employee and order objects

        Reservation maxReservation = new Reservation(new Customer("Maxwell Powers"), "8pm", "31.03.2022");

        Employee peter = new Employee("Peter Griffin", "Waiter");

        Employee lois = new Employee("Lois Griffin", "Cook");

        maxReservation.setWaiter(peter);

        // ordering food and drinks with addMethods

        Order orderMax = new Order();
        orderMax.addDrink(new Drink("Coke", 395));
        orderMax.addDrink(new Drink("Negroni Cocktail", 500));

        orderMax.addFood(new Food("Pizza Magherita", 1050));
        orderMax.addFood(new Food("Antipasti Selection", 970));

        // printing out farewell message to guest and total price

        System.out.println( "Dear Guest "+
                            maxReservation.getCustomer().getName() + ",\n" +
                            "We thank you so much for your business.\n" +
                            "Tonight you had " +
                            orderMax.getNumberOfDrinks() +
                            " drinks and you ordered " +
                            orderMax.getNumberOfFoods() +
                            " different variations of our food.\n" +
                            "Your total is " + orderMax.totalPrice() + " €");
    }
}
