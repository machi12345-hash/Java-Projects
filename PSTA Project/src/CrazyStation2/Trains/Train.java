package CrazyStation2.Trains;

import CrazyStation2.Cars.Car;
import CrazyStation2.CentralStation;
import CrazyStation2.Station;

import java.util.LinkedList;

//could work
// implemented lists, changed add remove and maxcar attached
public abstract class Train {
    private Station station;
    private CentralStation central;
    private int carNumber;
    private LinkedList<Car> cars;

    public Train (){};

    public Train (Station station, CentralStation central, int carNumber){
        this.central = central;
        this.station = station;
        this.carNumber = carNumber;
        this.cars = new LinkedList<>();
    }

    public LinkedList<Car> getCars() {
        return cars;
    }

    public Station getStation (){
        return station;
    }

    public CentralStation getCentral () {
        return central;
    }

    public int getCarNumber () {return carNumber;}

    public boolean addCar (Car c){
        
        if(cars.size() != carNumber) {
            cars.add(c);
            return true;
        }
        return false;
    }

    public Car removeCar (){
       
        return this.cars.removeLast();
    }

//should work
    public boolean maxCarAttached (){
        if (carNumber == cars.size()){
            return true;
        } else
            return false;
    }
}
