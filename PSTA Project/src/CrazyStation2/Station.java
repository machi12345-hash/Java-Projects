import java.util.Collections;
import java.util.LinkedList;

public class Station {
    private LinkedList<Car> storage; //
    private LinkedList<Train> trains;
    private String name;
    private LinkedList<Train> rentals;


    public Station (String name){
        this.name = name;
        this.storage = new LinkedList<>();
        this.trains = new LinkedList<>();
    }

    public Station (String name, Train train){
        this.name = name;
        this.storage = new LinkedList<>();
        this.trains = new LinkedList<>();
        trains.add(train);
    }


    public void addTrain (Train c) {
        
        trains.add(c);
    }

    public boolean addCar (Car c){
        
        if (storage.add(c)) {
            return true;
        }
        return false;
    }

    public Car removeCar (){
       
       return storage.removeLast();
    }

    public void loadTrains (){
       
        for (Train t: trains) {
            while (!t.maxCarAttached() && storage.size() != 0) {
                t.addCar(storage.remove());
            }
        }
    }

    public void unloadTrains () {
        for (Train t: trains){
            while (t.getCars().size() != 0) {
                storage.add(t.removeCar());
            }
        }
    }

  

    public LinkedList<Car> getStorage (){return storage; }

    public void sortStorage (){
        storage.sort(Car::compareTo);
        Collections.reverse(storage);
    }

    public LinkedList<Train> getTrains ()  { return trains; }

    public String getName() { return name; }

    public void setTrains (LinkedList trains) {this.trains = trains;}

    public void setRentals (LinkedList<Train> rentals) {this.rentals = rentals; }

    public LinkedList<Train> getRentals () {return rentals;}

    public void unloadRentals () {
        for (Train t: rentals){
            Car c = t.removeCar();
            while (c!=null){
                addCar(c);
                c = t.removeCar();
            }
        }
 
    }
}
