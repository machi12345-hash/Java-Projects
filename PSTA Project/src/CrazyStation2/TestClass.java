package CrazyStation2;
import CrazyStation2.Cars.Car;
import CrazyStation2.Cars.FoodCar;
import CrazyStation2.Cars.MaterialCar;
import CrazyStation2.Cars.ProductCar;
import CrazyStation2.Trains.ElectricLocomotive;
import CrazyStation2.Trains.FreightTrain;
import org.junit.jupiter.api.Test;

public class TestClass {

    @Test
    void testClass() {

        TrainRental rental = new TrainRental("i");

        Station hamburg = new Station ("Hamburg");
        Station berlin = new Station ("Berlin");
        Station munich = new Station ("Munich");
        Station cologne = new Station("Cologne");


        CentralStation x = new CentralStation("frankfrut");
        FreightTrain munich_frankfurt = new FreightTrain(munich, x);
        ElectricLocomotive hamburg_frankfurt = new ElectricLocomotive(hamburg, x);
        ElectricLocomotive hamburg_frankfurt2 = new ElectricLocomotive(hamburg, x);
        ElectricLocomotive berlin_frankfurt = new ElectricLocomotive(berlin, x);
        FreightTrain cologne_frankfurt = new FreightTrain(cologne, x);


        hamburg.addTrain(hamburg_frankfurt);
        munich.addTrain(munich_frankfurt);
        berlin.addTrain(berlin_frankfurt);
        hamburg.addTrain(hamburg_frankfurt2);


        x.addTrain(hamburg_frankfurt);
        x.addTrain(hamburg_frankfurt2);
        x.addTrain(berlin_frankfurt);
        x.addTrain(munich_frankfurt);


        FoodCar f4 = new FoodCar(4, hamburg, munich);
        ProductCar p2 = new ProductCar(6, hamburg, munich);
        ProductCar p3 = new ProductCar(7, hamburg, hamburg);
        MaterialCar m4 = new MaterialCar(12, hamburg, munich);
        MaterialCar m5 = new MaterialCar(11, hamburg, hamburg);
        FoodCar f3 = new FoodCar(3, hamburg, munich);
        FoodCar f1 = new FoodCar(1, munich, hamburg);
        ProductCar p9 = new ProductCar(9, munich, berlin);
        ProductCar p8 = new ProductCar(8, berlin, hamburg);
        FoodCar f10 = new FoodCar(10, munich, hamburg);
        ProductCar p13 = new ProductCar(13, berlin, hamburg);
        MaterialCar m15 = new MaterialCar(15, hamburg, hamburg);
        FoodCar f44 = new FoodCar(44, cologne, cologne);
        MaterialCar m45 = new MaterialCar(45, hamburg, cologne);
        ProductCar p46 = new ProductCar(46, berlin, cologne);
        FoodCar f47 = new FoodCar(47, munich, cologne);

        hamburg.addCar(m5);
        hamburg.addCar(f4);
        hamburg.addCar(p2);
        hamburg.addCar(p3);
        hamburg.addCar(m4);
        hamburg.addCar(f3);
        munich.addCar(f1);
        munich.addCar(p9);
        berlin.addCar(p8);
        munich.addCar(f10);
        berlin.addCar(p13);
        berlin.addCar(m15);
        x.addCar(f44);
        x.addCar(m45);
        x.addCar(p46);
        x.addCar(f47);

        hamburg.loadTrains();
        munich.loadTrains();
        berlin.loadTrains();


        System.out.println("---");
        System.out.println(berlin_frankfurt.getCars().toString());
        System.out.println("----");
        System.out.println(munich_frankfurt.getCars().toString());
        System.out.println("---");

        x.unloadTrains();
        System.out.println(x.getStorage().toString());
        x.sortStorage();
        System.out.println(x.getStorage().toString());
        x.distributeCars();
        x.rentTrains(rental,cologne);



        System.out.println("berlin frankfurt");
        System.out.println(berlin_frankfurt.getCars().toString());

        System.out.println("munich frankfurt");
        System.out.println(munich_frankfurt.getCars().toString());
        System.out.println("hamburg");
        System.out.println(hamburg_frankfurt.getCars().toString());
        System.out.println(hamburg_frankfurt2.getCars().toString());
        System.out.println("should be empty cause we rented all trains");
        System.out.println(cologne.getRentals().get(0).getCars().toString());
        System.out.println(x.getStorage().toString());



        }
    }

