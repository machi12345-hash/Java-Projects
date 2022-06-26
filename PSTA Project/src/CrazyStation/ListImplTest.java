package CrazyStation;


import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;


class ListImplTest {

    List<Car> cars = new ListImpl<Car>();
    @Test
    public void ListTest() {


       // creating new instances to test the list

        Car car1 = new Car(1, new Station("Station 1"), new Station( "station2"));
        Car car2 = new Car(2, new Station("Station3"), new Station("station 2"));
        Car car3 = new Car(3, new Station("Station4"), new Station("station 2"));
        Car car4 = new Car(4, new Station("Station6"), new Station("station 2"));
        Car car5 = new Car(5, new Station("Station7"), new Station("station 2"));
        
        cars.insert(car1);
        cars.insert(car2);
        cars.insert(car3);
        cars.insert(car4);
        cars.insert(car5);

        // test if insert method works
        assertEquals(5,cars.size());

        //tests contain and get node method
        assertTrue(cars.contains(cars.getNode(4)));

        //test if pop method works
        cars.popNode();
        assertEquals(4, cars.size());
        assertFalse(cars.contains(car1));


        //delete method test

        cars.deleteAt(2);
        assertFalse(cars.contains(car4));

    }







}
