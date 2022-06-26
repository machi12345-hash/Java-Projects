package CrazyStation2;

import CrazyStation2.Cars.FoodCar;
import CrazyStation2.Cars.MaterialCar;
import CrazyStation2.Cars.ProductCar;
import CrazyStation2.Trains.ElectricLocomotive;
import CrazyStation2.Trains.FreightTrain;
import CrazyStation2.Trains.SteamLocomotive;

public class CrazyStation2 {
    public static void main(String[] args) {

        // Setup
        TrainRental meyer = new TrainRental("Meyer's Trainrental");

        Station hamburg = new Station ("Hamburg");
        Station berlin = new Station ("Berlin");
        Station cologne = new Station ("Cologne");
        Station munich = new Station ("Munich");

        CentralStation frankfurt = new CentralStation("Frankfurt");

        FreightTrain munich_frankfurt = new FreightTrain(munich, frankfurt);
        ElectricLocomotive hamburg_frankfurt = new ElectricLocomotive(hamburg, frankfurt);
        ElectricLocomotive berlin_frankfurt = new ElectricLocomotive(berlin, frankfurt);
        SteamLocomotive cologne_frankfurt = new SteamLocomotive(cologne, frankfurt);
        SteamLocomotive cologne_frankfurt2 = new SteamLocomotive(cologne, frankfurt);

        hamburg.addTrain(hamburg_frankfurt);
        munich.addTrain(munich_frankfurt);
        cologne.addTrain(cologne_frankfurt);
        berlin.addTrain(berlin_frankfurt);

        cologne.addTrain(cologne_frankfurt2);

        frankfurt.addTrain(hamburg_frankfurt);
        frankfurt.addTrain(munich_frankfurt);
        frankfurt.addTrain(cologne_frankfurt);
        frankfurt.addTrain(berlin_frankfurt);

        frankfurt.addTrain(cologne_frankfurt2);

        FoodCar f1 = new FoodCar(1, hamburg, cologne);
        FoodCar f2 = new FoodCar(2, hamburg, cologne);
        FoodCar f3 = new FoodCar(3, hamburg, munich);
        FoodCar f4 = new FoodCar(4, hamburg, munich);
        ProductCar p1 = new ProductCar(5, munich, cologne);
        ProductCar p2 = new ProductCar(6, berlin, munich);
        ProductCar p3 = new ProductCar(7, berlin, hamburg);
        ProductCar p4 = new ProductCar(8, cologne, munich);
        MaterialCar m1 = new MaterialCar(9, munich, cologne);
        MaterialCar m2 = new MaterialCar(10, munich, berlin);
        MaterialCar m3 = new MaterialCar(11, cologne, berlin);
        MaterialCar m4 = new MaterialCar(12, berlin, munich);
        MaterialCar m5 = new MaterialCar(13, berlin, hamburg);
        FoodCar f5 = new FoodCar(14, berlin, munich);
        MaterialCar m6 = new MaterialCar(17, munich, cologne);


        hamburg.addCar(f1);
        hamburg.addCar(f2);
        hamburg.addCar(f3);
        hamburg.addCar(f4);
        munich.addCar(p1);
        berlin.addCar(p2);
        berlin.addCar(p3);
        cologne.addCar(p4);
        munich.addCar(m1);
        munich.addCar(m2);
        cologne.addCar(m3);
        berlin.addCar(m4);
        berlin.addCar(m5);
        berlin.addCar(f5);
        munich.addCar(m6);

        System.out.println("Situation at the beginning of the day:");
        System.out.println(hamburg);
        System.out.println(berlin.toString());
        System.out.println(munich.toString());
        System.out.println(cologne.toString());

        // Cars get attached to the available trains on those routes
        hamburg.loadTrains();
        cologne.loadTrains();
        munich.loadTrains();
        berlin.loadTrains();

        // Cars left in Frankfurt the day before
        FoodCar f6 = new FoodCar(15, berlin, cologne);
        ProductCar p5 = new ProductCar(16, berlin, cologne);
        frankfurt.addCar(f6);
        frankfurt.addCar(p5);
        System.out.println("\n\nCars left the day before:");
        System.out.print(frankfurt.toString());
        System.out.println("----------------------------------------------------\n");


        // Cars get transported from Stations to CentralStation Frankfurt
        frankfurt.unloadTrains();
        frankfurt.sortCars();
        System.out.println(frankfurt.toString());
        System.out.println("----------------------------------------------------\n");

        frankfurt.distributeCars();

        // Trains drive with the new attached cars back to the stations
        hamburg.unloadTrains();
        berlin.unloadTrains();
        munich.unloadTrains();
        cologne.unloadTrains();

        // Lets check if the cars are at the right station
        System.out.println(hamburg);
        System.out.println(berlin);
        System.out.println(munich);
        System.out.println(cologne);

        // What´s left at the CentralStation?
        System.out.println("\n________________Left in Frankfurt________________");
        System.out.print(frankfurt.toString());
/*
        // rental
        if (!munich_distributable){
            frankfurt.rentTrains(meyer, munich);
            munich.unloadRentals();
        }
        if (!hamburg_distributable){
            frankfurt.rentTrains(meyer, hamburg);
            hamburg.unloadRentals();
        }
        if (!berlin_distributable){
            frankfurt.rentTrains(meyer, berlin);
            berlin.unloadRentals();
        }
        if (!cologne_distributable){
            frankfurt.rentTrains(meyer, cologne);
            cologne.unloadRentals();
        }


 */


        System.out.println("-------------------------------------------------\n");

        // Lets check if the cars are at the right station
        System.out.println(hamburg.toString());
        System.out.println(berlin.toString());
        System.out.println(munich.toString());
        System.out.println(cologne.toString());

        // Is any car left at the Centralstation?
        System.out.println("\n\n________________Left in Frankfurt________________");
        System.out.print(frankfurt.toString());

    }


    }

