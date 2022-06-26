package CrazyStation2.Trains;

import CrazyStation2.CentralStation;
import CrazyStation2.Station;
import CrazyStation2.Trains.Train;

public class SteamLocomotive extends Train {
    public SteamLocomotive (Station station, CentralStation central){
        super (station, central, 3);
    }
}
