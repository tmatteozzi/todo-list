import java.util.ArrayList;
import java.sql.*;

public class ToDoListModel {
    // ATTRIBUTES FOR DB CONNECTION
    private String url = "jdbc:sqlite:/Users/tomasmatteozzi/Documents/workspaces/uni/ingenieria-de-software-2/todo-list/todo-list/src/todolist.db";
    private Connection connection = null;
    private ArrayList<Item> itemList;
    private ToDoList toDoList;

    public ToDoListModel() {
        try {
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection(url);
            if (connection!=null){
                System.out.println("Conexion exitosa a la BD.");
            }
        } catch (ClassNotFoundException | SQLException e) {
            System.out.println(e.getMessage());
        }
        toDoList = new ToDoList();
        itemList = toDoList.getAllItems();
    }

    public void addItem(Item item) {
        try{
            String sql = "INSERT INTO Item (description, done, date) VALUES (?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.setBoolean(2, item.isDone());
            statement.setDate(3, Date.valueOf(item.getDate()));
            statement.executeUpdate();
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }

    public void deleteItem(Item item) {
        try{
            String sql = "DELETE FROM Item WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            // IF I DELETE IT SUM 1
            int deleted = statement.executeUpdate();
            statement.close();
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }

    public void finishItem(Item item) {
        try{
            String sql = "UPDATE Item SET done = 1 WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.executeUpdate();
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }

    public ArrayList<Item> getAllItems() {
        return itemList;
    }

    public ArrayList<Item> getUnfinishedItems() {
        ArrayList<Item> unfinishedItems = new ArrayList<>();
        for (Item item : itemList) {
            if (!item.isDone()) {
                unfinishedItems.add(item);
            }
        }
        return unfinishedItems;
    }

    public ArrayList<Item> getCompletedItems() {
        ArrayList<Item> completedItems = new ArrayList<>();
        for (Item item : itemList) {
            if (item.isDone()) {
                completedItems.add(item);
            }
        }
        return completedItems;
    }
}
