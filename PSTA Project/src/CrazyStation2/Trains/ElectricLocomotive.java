package CrazyStation2.Trains;

import CrazyStation2.CentralStation;
import CrazyStation2.Station;
import CrazyStation2.Trains.Train;

public class ElectricLocomotive extends Train {
    public ElectricLocomotive (Station station, CentralStation central){
        super (station, central, 5);
    }
}
