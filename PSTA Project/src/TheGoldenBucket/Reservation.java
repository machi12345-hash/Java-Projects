package TheGoldenBucket;

public class Reservation {

    // DATA 

    private Customer customer; // changed c to customer from readability sake
    private String time;
    private String date;
    private Employee waiter;
    private Order[] orders;

    // CONSTRUCTORS

    public Reservation(Customer customer, String time, String date) {
        this.customer = customer;
        this.time = time;
        this.date = date;
    }
    
    // METHODS

    void addOrder(Order o){
        Utilities.enlargeOrderArray(orders);
        orders[orders.length]=o;
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public String getTime() {
        return time;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public Employee getWaiter() {
        return waiter;
    }

    public void setWaiter(Employee waiter) {
        this.waiter = waiter;
    }

    public Order[] getOrders() {
        return orders;
    }

    public void setOrders(Order[] orders) {
        this.orders = orders;
    }
}
