package CrazyStation;

public class CrazyStation {

    public static void main(String[] args) {

        //creating all the lists
        List<Car> storage_cologne = new ListImpl<Car>();
        List<Car> storage_hamburg = new ListImpl<Car>();
        List<Car> storage_berlin = new ListImpl<Car>();
        List<Car> storage_frankfurt = new ListImpl<Car>();
        List<Car> storage_munich = new ListImpl<Car>();
        List<Train> trainStorage = new ListImpl<Train>();

        // creating station objects
        Station munich = new Station("Munich", storage_munich);
        Station hamburg = new Station("Hamburg", storage_hamburg);
        Station berlin = new Station("Berlin", storage_berlin);
        Station cologne = new Station("Cologne", storage_cologne);
        CentralStation frankfurt = new CentralStation("Frankfurt", storage_frankfurt, trainStorage);

        //creating train objects
        Train hamburg_frankfurt = new Train(hamburg, frankfurt);
        Train berlin_frankfurt = new Train(berlin, frankfurt);
        Train munich_frankfurt = new Train(munich, frankfurt);
        Train cologne_frankfurt = new Train(cologne, frankfurt);
        hamburg.setTrain(hamburg_frankfurt);
        berlin.setTrain(berlin_frankfurt);
        munich.setTrain(munich_frankfurt);
        cologne.setTrain(cologne_frankfurt);
        frankfurt.addTrain(berlin_frankfurt);
        frankfurt.addTrain(hamburg_frankfurt);
        frankfurt.addTrain(cologne_frankfurt);
        frankfurt.addTrain(munich_frankfurt);


        //creating Car objects and inserting them into lists
        storage_hamburg.insert(new Car(1,hamburg,cologne));
        storage_hamburg.insert(new Car(3, hamburg, munich));
        storage_hamburg.insert(new Car(4, hamburg, munich));
        storage_hamburg.insert(new Car(2, hamburg,cologne));
        storage_berlin.insert(new Car(6, berlin, munich));
        storage_berlin.insert(new Car(7, berlin, hamburg));
        storage_berlin.insert(new Car(12, berlin, munich));
        storage_berlin.insert(new Car(13, berlin, hamburg));
        storage_berlin.insert(new Car(14, berlin, munich));
        storage_cologne.insert(new Car(11, cologne, berlin));
        storage_cologne.insert(new Car(8, cologne, munich));
        storage_munich.insert(new Car(5, munich, cologne));
        storage_munich.insert(new Car(9, munich, cologne));
        storage_munich.insert(new Car(10, munich, berlin));
        hamburg.setStorage(storage_hamburg);
        berlin.setStorage(storage_berlin);
        munich.setStorage(storage_munich);
        cologne.setStorage(storage_cologne);


        printStart(hamburg);
        printStart(cologne);
        printStart(munich);
        printStart(berlin);


        hamburg_frankfurt.loadTrain();
        berlin_frankfurt.loadTrain();
        munich_frankfurt.loadTrain();
        cologne_frankfurt.loadTrain();

        hamburg_frankfurt.unloadTrain();
        berlin_frankfurt.unloadTrain();
        cologne_frankfurt.unloadTrain();
        munich_frankfurt.unloadTrain();


        System.out.println("__________Arrived and Offloaded in Frankfurt__________");
        frankfurt.getStorage().printAll();

        System.out.println("_________________________________________");

        berlin_frankfurt = frankfurt.refillTrain(berlin_frankfurt);
        hamburg_frankfurt = frankfurt.refillTrain(hamburg_frankfurt);
        cologne_frankfurt = frankfurt.refillTrain(cologne_frankfurt);
        munich_frankfurt = frankfurt.refillTrain(munich_frankfurt);

        printTrains(hamburg_frankfurt);
        printTrains(munich_frankfurt);
        printTrains(cologne_frankfurt);
        printTrains(berlin_frankfurt);

        hamburg_frankfurt.unloadTrain(hamburg);
        berlin_frankfurt.unloadTrain(berlin);
        cologne_frankfurt.unloadTrain(cologne);
        munich_frankfurt.unloadTrain(munich);


        printStation(hamburg);
        printStation(munich);
        printStation(berlin);
        printStation(cologne);

    }

    public static void printStart(Station station) {
        System.out.println("__________Start of the Day in "+ station.getName() +"__________");
        station.getStorage().printAll();
        System.out.println();
    }

    public static void printTrains(Train train) {
        System.out.println("__________Train to "+ train.getStation().getName()+" successfully loaded__________");
        train.getWagons().printAll();
        System.out.println();
    }

    public static void printStation(Station station) {
        System.out.println("__________Wagons succesfully offloaded at: "+ station.getName()+" __________");
        station.getStorage().printAll();
        System.out.println();
    }
}
