package CrazyStation2;

import CrazyStation2.Trains.ElectricLocomotive;
import CrazyStation2.Trains.FreightTrain;
import CrazyStation2.Trains.SteamLocomotive;
import CrazyStation2.Trains.Train;

import java.util.LinkedList;

public class TrainRental {
    String name;

    public TrainRental (String name){
        this.name = name;
    }

    public LinkedList<Train> lendTrain (int necessaryCap, Station station, CentralStation central){
        LinkedList<Train> rentals = new LinkedList<>();
    
        if (necessaryCap <= 3) {
            rentals.add(new SteamLocomotive(station,central));
        } else if (necessaryCap > 3 && necessaryCap <= 5) {
            rentals.add(new ElectricLocomotive(station, central));
        } else {
            rentals.add(new FreightTrain(station,central));
        }


        return rentals;
    }
}
