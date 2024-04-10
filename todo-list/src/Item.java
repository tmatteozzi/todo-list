import java.time.LocalDate;

public class Item {
    // ATTRIBUTES
    private int id;
    private String description;
    private boolean done;
    private LocalDate date;

    // NEW ITEM CONSTRUCTOR
    public Item(String description){
        this.description = description;
        try{
            if(description != null){
                done = false;
                date = LocalDate.now();
            }
            else{
                throw new Exception("DESCRIPTION CANNOT BE EMPTY.");
            }
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }

    // CONSTRUCTOR FOR SQL QUERY
    public Item(int id, String description, boolean done, LocalDate date){
        this.id = id;
        this.description = description;
        this.done = done;
        this.date = date;
    }
    public int getId() { return id; }
    public String getDescription() { return description; }
    public boolean isDone() { return done; }
    public LocalDate getDate() { return date; }
}
