package CrazyStation2.Cars;

import CrazyStation2.Cars.Car;
import CrazyStation2.Station;

public class ProductCar extends Car {

    public ProductCar(int carID, Station station, Station target){
        super (carID, station, target, 2);
    }
}
