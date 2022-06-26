package CrazyStation2;

import CrazyStation2.Cars.Car;
import CrazyStation2.Trains.Train;

import java.util.LinkedList;

public class CentralStation extends Station {


    public CentralStation (String name){
        super (name);
    }


    public void sortCars (){
        super.sortStorage();
    }



    public void distributeCars () {
        for (Train t: getTrains()) {
            for (int i = 0; i < getStorage().size(); i++) {
                Car c = getStorage().get(i);
                if (c.getTarget().getName().equals(t.getStation().getName()) && !t.maxCarAttached()) {
                    t.addCar(c);
                    getStorage().remove(c);
                    i--;
                }
            }
        }
    }


    public void rentTrains (TrainRental trainRental, Station station) {
        int required = 0;

        if (super.getStorage() == null)
            return;
        for (Car c: super.getStorage()){
            if (c.getTarget() == station) {
                required++;
            }
        }
        LinkedList<Train> abc = trainRental.lendTrain(required,station,this);
        super.setRentals(abc);
        LinkedList<Train> trains = super.getTrains();
        super.setTrains(super.getRentals());
        distributeCars();
        station.setRentals(super.getRentals());
        super.setTrains(trains);
    }


}
