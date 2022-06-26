package Titanic;

import java.io.IOException;
import java.util.*;

public class TitanicAnalyse {

    private List<Ticket> tickets = new LinkedList<>();

    public TitanicAnalyse() throws IOException {
        this.tickets = TitanicStatistics.loadData();
    }


    //sorts the most frequent Surnames and returns the position you want

    public String mostFrequentSurname(int rank) {
        HashMap<String, Integer> MapOfSurnames = new HashMap<>();

        if (rank == 0) {
            throw new NoSuchElementException("1 is the highest rank");
        }

        for (Ticket t : tickets) {
            if (!MapOfSurnames.containsKey(t.getSurname())) {
                MapOfSurnames.put(t.getSurname(), 1);
            } else {
                int i = MapOfSurnames.get(t.getSurname());
                MapOfSurnames.replace(t.getSurname(), ++i);
            }
        }

        LinkedList<String> surnamesList = new LinkedList<>(MapOfSurnames.keySet());
        surnamesList.sort((o1, o2) -> MapOfSurnames.get(o2) - MapOfSurnames.get(o1));

        return surnamesList.get(rank - 1);
    }

    //sorts the most frequent Ages and returns the position you want

    public int mostFrequentAge(int rank) {
        HashMap<Integer, Integer> MapOfAges = new HashMap<>();

        if (rank == 0) {
            throw new NoSuchElementException("1 is the highest rank");
        }

        for (Ticket t : tickets) {
            if (!MapOfAges.containsKey(t.getAge()) && t.getAge() != -1) {
                MapOfAges.put(t.getAge(), 1);
            } else if (!(t.getAge() == -1)) {
                int i = MapOfAges.get(t.getAge());
                MapOfAges.replace(t.getAge(), ++i);
            }
        }

        LinkedList<Integer> ageList = new LinkedList<>(MapOfAges.keySet());
        ageList.sort((o1, o2) -> (MapOfAges.get(o2) - MapOfAges.get(o1)));


        return ageList.get(rank - 1);
    }


    //calculates the percentage of deceased of each PClass

    public double percentageDeceasedPClass(String pClass) {
        LinkedList<Ticket> deceased = new LinkedList<>();
        LinkedList<Ticket> alive = new LinkedList<>();

        if (pClass.compareTo("1st") == 0 ||
                pClass.compareTo("2nd") == 0 ||
                pClass.compareTo("3rd") == 0) {


            for (Ticket t : tickets) {
                if (t.getPclass().compareTo(pClass) == 0) {
                    if (t.getSurvived() == 1) {
                        alive.add(t);
                    } else {
                        deceased.add(t);
                    }
                }
            }

            double deacesedSize = deceased.size();
            double aliveSize = alive.size();

            return deacesedSize / (aliveSize + deacesedSize);
        } else {
            throw new NoSuchElementException();
        }
    }

     public double averageAgePassengers() {
        int passengers = 0;
         int totalAge = 0;
         for (Ticket t : tickets) {
             if (t.getAge() != -1) {
                 passengers++;
                 totalAge += t.getAge();
             }

         }
         double averageAge = (double) totalAge / (double) passengers;

         return averageAge;

     }


    public double percentageDeceasedPeopleInTwenties() {
        LinkedList<Ticket> deceased = new LinkedList<>();
        LinkedList<Ticket> alive = new LinkedList<>();

        for (Ticket t : tickets) {
            if (t.getAge() != -1 && t.getAge() > 19 && t.getAge() < 30) {
                if (t.getSurvived() == 0) {
                    deceased.add(t);
                } else
                    alive.add(t);
            }

        }
        double deceasedSize = deceased.size();
        double aliveSize = alive.size();

        return deceasedSize / (aliveSize + deceasedSize);

    }
    public int numberOfPassengers(){
        return tickets.size();
    }
}
