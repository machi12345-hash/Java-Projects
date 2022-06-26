package CrazyStation;

public class CentralStation {
    private List<Car> storage;
    private List<Train> trains;
    private String name;

    public CentralStation(String name, List<Car> storage, List<Train> trainStorage) {
        this.name = name;
        this.storage = storage;
        this.trains = trainStorage;
    }

    public void printStorage () {
        String s;
        s = name + ":\n";
        System.out.println(s);
        storage.printAll();

    }

    //adds train to centralhub
    public void addTrain(Train train) {
        trains.insert(train);
    }

    //fills the trains with wagons
    public Train refillTrain(Train t) {
        int sizeS = storage.size();
        int sizeT = trains.size();
        Train returnTrain = null;
        List<Car> temp = new ListImpl<Car>();

        for (int i = 0; i < sizeT; i++) {
            if (t.getStation().equals(trains.getNode(i).getStation())) {
                returnTrain = trains.getNode(i);
                trains.deleteAt(i);
            }
        }

        for (int i = 0; i < sizeS; i++) {
            Car tempCar = storage.popNode();
            if (returnTrain.getStation().equals(tempCar.getTarget())) {
                temp.insert(tempCar);

            } else {
                storage.insert(tempCar);
            }

        }
        returnTrain.setWagons(temp);

        return returnTrain;
    }



    public List<Car> getStorage() {
        return storage;
    }

    public void setStorage(List<Car> storage) {
        this.storage = storage;
    }

    public List<Train> getTrains() {
        return trains;
    }

    public void setTrains(List<Train> trains) {
        this.trains = trains;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }


}
