package Titanic;

public class Ticket {
    private String surname;
    private String name;
    private String pclass;
    private int age;
    private String sex;
    private int survived;

    public Ticket(String surname, String name, String pclass, int age, String sex, int survived) {
        this.surname = surname;
        this.name = name;
        this.pclass = pclass;
        this.age = age;
        this.sex = sex;
        this.survived = survived;
    }

    public String toString(){
        return surname+" "+name+" "+pclass+" "+age+" "+sex+" "+survived;
    }

    public int compareTo (Ticket t){
        if (t.age > age){
            return 1;
        } else if (t.age == age){
            if (t.surname.compareTo(surname) == 0){
                return t.name.compareTo(name);
            }
            else {
                return t.surname.compareTo(surname);
            }
        } else
            return -1;
    }

    public int getAge () {return age;}
    public int getSurvived () {return survived;}
    public String getSex () {return sex;}
    public String getPclass () {return pclass;}
    public String getSurname () {return surname;}
    public String getName () {return name;}
}
