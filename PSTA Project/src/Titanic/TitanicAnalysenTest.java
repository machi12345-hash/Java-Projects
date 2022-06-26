package Titanic;

import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.LinkedList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class TitanicAnalysenTest {
    @Test
    void sortByAgeAndAlphabet() throws IOException {
        List<Ticket> tickets = TitanicStatistics.loadData();
        Ticket[] ticketArray = new Ticket[tickets.size()];
        tickets.toArray(ticketArray);
        int n = ticketArray.length;
        Ticket temp;
        for(int i=0; i < n; i++){
            for(int j=1; j < (n-i); j++){
                if(ticketArray[j-1].compareTo(ticketArray[j]) < 0){
                    temp = ticketArray[j-1];
                    ticketArray[j-1] = ticketArray[j];
                    ticketArray[j] = temp;
                }
            }
        }

        assertEquals("Andrew  Mr Frank 2nd -1 male 0", ticketArray[0].toString());
        assertEquals("Hagland  Mr Ingvald Olsen 3rd -1 male 0", ticketArray[100].toString());
        assertEquals("Makinen  Mr Kalle Edvard 3rd -1 male 0", ticketArray[200].toString());
        assertEquals("Odahl  Mr Nils Martin 3rd -1 male 1", ticketArray[300].toString());
        assertEquals("Ryan  Mr Patrick 3rd -1 male 0", ticketArray[400].toString());
        assertEquals("Todoroff  Mr Lalio 3rd -1 male 0", ticketArray[500].toString());
    }

    @Test
    void sortMenByAge() throws IOException {
        List<Ticket> tickets = TitanicStatistics.loadData();
        List<Ticket> allMen = new LinkedList<>();
        for (Ticket t: tickets){
            if (t.getSex().compareTo("male") == 0){
                allMen.add(t);
            }
        }

        Ticket[] ticketArray = new Ticket[allMen.size()];
        allMen.toArray(ticketArray);
        int n = ticketArray.length;
        Ticket temp;
        for(int i=0; i < n; i++){
            for(int j=1; j < (n-i); j++){
                if(ticketArray[j-1].compareTo(ticketArray[j]) < 0){
                    temp = ticketArray[j-1];
                    ticketArray[j-1] = ticketArray[j];
                    ticketArray[j] = temp;
                }
            }
        }

        assertEquals(851, ticketArray.length);
        assertEquals("Andrew  Mr Frank 2nd -1 male 0", ticketArray[0].toString());
        assertEquals("Khalil  Mr Saad 3rd -1 male 0", ticketArray[100].toString());
        assertEquals("Olsson  Mr Nils Johan 3rd -1 male 0", ticketArray[200].toString());
        assertEquals("Sholt  Mr Peter Andreas Lauritz Andersen 3rd -1 male 0", ticketArray[300].toString());
        assertEquals("Johnson  Master Harold Theodor 3rd 4 male 1", ticketArray[400].toString());
        assertEquals("Johansson  Mr Erik 3rd 22 male 0", ticketArray[500].toString());


    }

    @Test
    void sortChildrenByAgeAndAlphabet() throws IOException {
        List<Ticket> tickets = TitanicStatistics.loadData();
        List<Ticket> children = new LinkedList<>();
        for (Ticket t: tickets){
            if (t.getAge()>-1 && t.getAge()<18 ){
                children.add(t);
            }
        }

        Ticket[] ticketArray = new Ticket[children.size()];
        children.toArray(ticketArray);
        int n = ticketArray.length;
        Ticket temp;
        for(int i=0; i < n; i++){
            for(int j=1; j < (n-i); j++){
                if(ticketArray[j-1].compareTo(ticketArray[j]) < 0){
                    temp = ticketArray[j-1];
                    ticketArray[j-1] = ticketArray[j];
                    ticketArray[j] = temp;
                }
            }
        }
        assertEquals(96, ticketArray.length);
        assertEquals("Aks  Master Philip 3rd 0 male 1", ticketArray[0].toString());
        assertEquals("Klasen  Miss Gertrud Emilia 3rd 1 female 0", ticketArray[10].toString());
        assertEquals("Aspland  Master Edvin Rojj Felix 3rd 3 male 1", ticketArray[20].toString());
        assertEquals("Carr  Miss Helen 3rd 16 female 1", ticketArray[75].toString());

    }

    @Test
    void averageAgePassengers() throws IOException {
        TitanicAnalyse ta = new TitanicAnalyse();
        try {
            assertEquals(30.3915, ta.averageAgePassengers(), 0.001);
        } catch (Exception e) {
            System.out.println("Only the average age of the passengers");

        }
    }

    @Test
    void averageAgeDeceased() throws IOException {
        List<Ticket> tickets = TitanicStatistics.loadData();
        int passengers = 0;
        int totalAge = 0;
        for (Ticket t: tickets){
            if (t.getAge()!=-1 && t.getSurvived()==1){
                passengers++;
                totalAge += t.getAge();
            }
        }
        double averageAge = (double)totalAge / (double)passengers;
        assertEquals(29.348, averageAge, 0.001);
    }

    @Test
    void numberOfPassengers() throws IOException {

        TitanicAnalyse ta = new TitanicAnalyse();


            assertEquals(1313, ta.numberOfPassengers());

    }




    @Test
    void percentageDeceasedPeopleInTwenties() throws IOException {
        TitanicAnalyse ta = new TitanicAnalyse();
        try{
            assertEquals(0.666, ta.percentageDeceasedPeopleInTwenties(),0.001 );
        }catch (Exception e){
            System.out.println("Only deceased people in the twenties ");
            fail();

        }
    }

    @Test
    void averageAgeMen() throws IOException {
        List<Ticket> tickets = TitanicStatistics.loadData();
        int men = 0;
        int totalAge = 0;
        for (Ticket t: tickets){
            if (t.getAge()!=-1 && t.getSex() == "male"){
                men++;
                totalAge += t.getAge();
            }
        }
        double averageAge = (double)totalAge / (double)men;

        assertEquals(31.00, averageAge, 0.01);
    }

    @Test
    void averageAgeWomen() throws IOException {
        List<Ticket> tickets = TitanicStatistics.loadData();
        int women = 0;
        int totalAge = 0;
        for (Ticket t: tickets){
            if (t.getAge()!=-1 && t.getSex() == "female"){
                women++;
                totalAge += t.getAge();
            }
        }
        double averageAge = (double)totalAge / (double)women;
        assertEquals(29.39, averageAge, 0.01);
    }

    @Test
    void mostFrequentSurname() throws IOException {

        TitanicAnalyse ta = new TitanicAnalyse();

        try {
            assertEquals("Sage", ta.mostFrequentSurname(1));
            assertEquals("Andersson", ta.mostFrequentSurname(2));
            assertEquals("Goodwin", ta.mostFrequentSurname(3));
            assertEquals("Asplund", ta.mostFrequentSurname(4));

        } catch (Exception e) {
            System.out.println("1 is the highest rank");
            fail();
        }

    }




    @Test
    void mostFrequentAge() throws IOException {

        TitanicAnalyse ta = new TitanicAnalyse();

        try {

        assertEquals(22, ta.mostFrequentAge(1));
        assertEquals(21, ta.mostFrequentAge(2));
        assertEquals(30, ta.mostFrequentAge(3));
        assertEquals(18, ta.mostFrequentAge(4));

        } catch (Exception e) {
            System.out.println("1 is the highest rank");
            fail();
        }

    }

    @Test
    void percentageDeceasedPclass() throws IOException {

        TitanicAnalyse ta = new TitanicAnalyse();

        try {

            assertEquals(0.4006, ta.percentageDeceasedPClass("1st"), 0.01);
            assertEquals(0.575, ta.percentageDeceasedPClass("2nd"), 0.01);
            assertEquals(0.806, ta.percentageDeceasedPClass("3rd"), 0.01);

        } catch (Exception e) {
            System.out.println("There are only 1,2 and 3rd class");
            fail();
        }
    }
}

