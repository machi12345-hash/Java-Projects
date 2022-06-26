package TheGoldenBucket;

public class Employee {

    // DATA

    private String name;
    private String title;

    // CONSTRUCTOR

    public Employee(String name, String title) {
        this.name = name;
        this.title = title;
    }

    // METHODS


    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }
}
