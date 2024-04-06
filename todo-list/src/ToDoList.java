import javax.swing.*;
import java.sql.*;
import java.util.ArrayList;

public class ToDoList {
    // ATTRIBUTES FOR DB CONNECTION
    private String url = "jdbc:sqlite:/Users/tomasmatteozzi/Documents/workspaces/uni/ingenieria-de-software-2/todo-list/todo-list/src/todolist.db";
    private Connection connection = null;

    public ToDoList(){
        try {
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection(url);
            if (connection!=null){
                System.out.println("Conexion exitosa a la BD.");
            }
        } catch (ClassNotFoundException | SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void addItem(Item item){
        try{
            String sql = "INSERT INTO Item (description, done, date) VALUES (?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.setBoolean(2, item.isDone());
            statement.setDate(3, Date.valueOf(item.getDate()));
            statement.executeUpdate();
            JOptionPane.showMessageDialog(null, "ITEM ADDED SUCCESSFULLY.");
        } catch (Exception e){
            JOptionPane.showMessageDialog(null, e.getMessage());
        }
    }

    public void deleteItem(Item item){
        try{
            String sql = "DELETE FROM Item WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            // IF I DELETE IT SUM 1
            int deleted = statement.executeUpdate();
            statement.close();
            if (deleted > 0) {
                JOptionPane.showMessageDialog(null, "ITEM DELETED SUCCESSFULLY");
            } else {
                throw new Exception("THERE IS NO ITEM WITH THE DESCRIPTION PROVIDED.");
            }
        } catch (Exception e){
            JOptionPane.showMessageDialog(null, e.getMessage());
        }
    }

    public void finishItem(Item item){
        try{
            String sql = "UPDATE Item SET done = 1 WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.executeUpdate();
            JOptionPane.showMessageDialog(null, "TASK FINISHED.");
        } catch (Exception e){
            JOptionPane.showMessageDialog(null, e.getMessage());
        }
    }

    public ArrayList<Item> getAllItems(){
        ArrayList<Item> itemList = new ArrayList<>();
        try{
            // SELECT ALL ITEMS AND SAVE THEM IN A RESULTSET
            String sql = "SELECT * FROM Item";
            PreparedStatement statement = connection.prepareStatement(sql);
            ResultSet resultSet = statement.executeQuery();
            // ADD EACH ONE TO THE ITEM LIST
            while(resultSet.next()){
                String description = resultSet.getString("description");
                boolean done = resultSet.getBoolean("done");
                Date date = resultSet.getDate("date");
                Item item = new Item(description, done, date.toLocalDate());
                itemList.add(item);
            }
            resultSet.close();
            statement.close();
        } catch (Exception e){
            JOptionPane.showMessageDialog(null, e.getMessage());
        }
        return itemList;
    }
}
