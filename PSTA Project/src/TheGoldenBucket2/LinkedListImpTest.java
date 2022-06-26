package TheGoldenBucket2;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import static org.junit.Assert.assertEquals;

public class LinkedListImpTest {

    LinkedList<Drink> drinks= new LinkedListImpl<>();

    @Test
    public void LinkedListImpTest(){

        Drink coke = new Drink("Coke", 3);
        Drink latte= new Drink("latte", 8);
        Drink bier= new Drink("bier", 6);
        Drink whiskey= new Drink("Whiskey", 15);


        drinks.insert(coke);
        drinks.insert(latte);
        drinks.insert(bier);
        drinks.insert(whiskey);

//check if insert works
        assertEquals(4, drinks.size());

        //check if remove works
        drinks.remove();
        assertEquals(3, drinks.size());

        // check if retrieve at method works
        assertEquals(drinks.retrieveAt(2), bier);


        //test show method, should print out all items in the order
        drinks.show();

        //test the iterators
        int counter = 0;
        for (Drink d: drinks) {
            counter++;
        }
        assertEquals(3, counter);
       




    }


}
