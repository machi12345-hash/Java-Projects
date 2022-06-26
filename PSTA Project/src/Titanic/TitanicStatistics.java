package Titanic;

import org.simpleflatmapper.csv.CsvParser;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.List;
import java.util.stream.Collectors;

public class TitanicStatistics {
    public static void main(String[] args) throws IOException {
        System.out.println(loadData());
    }
    static public List<Ticket> loadData() throws IOException {
        ClassLoader classLoader = TitanicStatistics.class.getClassLoader();
        Reader reader = new InputStreamReader(classLoader.getResourceAsStream("Titanic/titanic.csv"));
        return  CsvParser
                .separator(';')
                .mapTo(Ticket.class)
                .stream(reader)
                .collect(Collectors.toList());
    }
}
