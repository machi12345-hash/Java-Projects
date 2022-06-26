package TheGoldenBucket;

public class Order {

    // DATA

    private Customer c;
    private Reservation r;
    private Drink[] drinks;
    private Food[] foods;
    private int numberOfDrinks;
    private int numberOfFoods;

    // CONSTRUCTORS

    public Order(){
        this.drinks= new Drink[0];
        this.foods = new Food[0];
        this.numberOfDrinks=0;
        this.numberOfFoods=0;
    }
    
    // METHODS

    double totalPrice() {

        double totalPrince = 0;

        for (Drink drink : drinks) {
            totalPrince = totalPrince + drink.getPrice();
        }
        for (Food food: foods) {
            totalPrince = totalPrince + food.getPrice();
        }

        return totalPrince/100;
    }

    void addDrink(Drink d){
        this.drinks =  Utilities.enlargeDrinkArray(drinks);
        drinks[drinks.length-1]=d;
        numberOfDrinks++;
    }

    void addFood(Food f){
        this.foods = Utilities.enlargeFoodArray(foods);
        foods[foods.length-1]=f;
        numberOfFoods++;
    }

    public Customer getC() {
        return c;
    }

    public void setC(Customer c) {
        this.c = c;
    }

    public Reservation getR() {
        return r;
    }

    public void setR(Reservation r) {
        this.r = r;
    }

    public Drink[] getDrinks() {
        return drinks;
    }

    public void setDrinks(Drink[] drinks) {
        this.drinks = drinks;
    }

    public Food[] getFoods() {
        return foods;
    }

    public void setFoods(Food[] foods) {
        this.foods = foods;
    }

    public int getNumberOfDrinks() {
        return numberOfDrinks;
    }

    public void setNumber_of_drinks(int numberOfDrinks) {
        this.numberOfDrinks = numberOfDrinks;
    }

    public int getNumberOfFoods() {
        return numberOfFoods;
    }

    public void setNumber_of_foods(int numberOfFoods) {
        this.numberOfFoods = numberOfFoods;
    }

}

