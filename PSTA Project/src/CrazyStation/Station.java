package CrazyStation;

public class Station {

    private List<Car> storage;
    private Train train;
    private String name;

    Station(String name, List<Car> storage) {
        this.name = name;
        this.storage = storage;
        this.train = null;
    }

    public Station(String station4) {

    }

    public void setTrain(Train train) {
        this.train = train;
    }

    public void setStorage(List<Car> cars) {
        this.storage = cars;
    }


    public void printStorage () {
        String s;
        s = name + ":\n";
        System.out.println(s);
        storage.printAll();

    }


    public List<Car> getStorage() {
        return storage;
    }

    public Train getTrain() {
        return train;
    }

    public String getName() {
        return name;
    }
}
