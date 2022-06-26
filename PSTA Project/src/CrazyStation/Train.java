package CrazyStation;

public class Train {

    private Station station;
    private CentralStation central;
    private List<Car> wagons;

    public Train(Station station, CentralStation central) {
        this.station=station;
        this.central=central;
    }

    //loads train from storage
    public void loadTrain() {
        this.wagons = station.getStorage();
        station.setStorage(null);
    }

    //unloads everything in central
    public void unloadTrain() {
        int size = wagons.size();
        for(int i = 0; i < size; i++) {
            central.getStorage().insert(wagons.popNode());
        }

    }

    public void unloadTrain(Station station) {
        List<Car> temp = new ListImpl<Car>();
        for(int i = 0; i < wagons.size(); i++) {
          temp.insert(wagons.popNode());
        }
        this.station.setStorage(temp);
    }

    public Station getStation() {
        return station;
    }

    public void setStation(Station station) {
        this.station = station;
    }

    public CentralStation getCentral() {
        return central;
    }

    public void setCentral(CentralStation central) {
        this.central = central;
    }

    public List<Car> getWagons() {
        return wagons;
    }
    public void setWagons(List<Car> wagons) { this.wagons = wagons;
    }
}
