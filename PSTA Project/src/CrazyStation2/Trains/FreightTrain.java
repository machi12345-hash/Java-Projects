package CrazyStation2.Trains;

import CrazyStation2.CentralStation;
import CrazyStation2.Station;
import CrazyStation2.Trains.Train;

public class FreightTrain extends Train {
    public FreightTrain (Station station, CentralStation central){
        super (station, central, 10);
    }
}
