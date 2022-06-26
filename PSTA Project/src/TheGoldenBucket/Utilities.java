package TheGoldenBucket;

public class Utilities {

    // Methods for adding 1 more Element to Food,Drink and Order Array

    static Food[] enlargeFoodArray(Food[] foodArray){
        Food[] returnArray = new Food[foodArray.length+1];
        int i=0;
        for(Food f : foodArray){
            returnArray[i++]=f;
        }
        return returnArray;
    }

    static Drink[] enlargeDrinkArray(Drink[] drinkArray){
        Drink[] returnArray = new Drink[drinkArray.length+1];
        int i=0;
        for(Drink f : drinkArray){
            returnArray[i++]=f;
        }
        return returnArray;
    }

    static Order[] enlargeOrderArray(Order[] orderArray){
        Order[] returnArray = new Order[orderArray.length+1];
        int i=0;
        for(Order f : orderArray){
            returnArray[i++]=f;
        }
        return returnArray;
    }
}
