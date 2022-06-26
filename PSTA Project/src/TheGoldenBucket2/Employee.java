package TheGoldenBucket2;

public class Employee extends Person{
    String title;

    public Employee (String name, String title){
        super(name);
        this.title = title;
    }

    public String getName (){
        return name;
    }

    public String getTitle (){
        return title;
    }
}
