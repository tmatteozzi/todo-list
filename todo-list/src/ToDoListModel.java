import java.util.ArrayList;
import java.sql.*;

public class ToDoListModel {
    // ATTRIBUTES FOR DB CONNECTION
    private String url = "jdbc:sqlite:/Users/tomasmatteozzi/Documents/workspaces/uni/ingenieria-de-software-2/todo-list/todo-list/src/todolist.db";
    private Connection connection = null;
    private ArrayList<Item> itemList;

    public ToDoListModel() {
        try {
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection(url);
            if (connection != null) {
                System.out.println("Conexion exitosa a la BD.");
            }
        } catch (ClassNotFoundException | SQLException e) {
            System.out.println(e.getMessage());
        }
        itemList = new ArrayList<>();
        loadItemsFromDatabase(); // Load items from the database
    }

    private void loadItemsFromDatabase() {
        try {
            String sql = "SELECT * FROM Item";
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);

            while (resultSet.next()) {
                String description = resultSet.getString("description");
                boolean done = resultSet.getBoolean("done");
                Date date = resultSet.getDate("date");
                itemList.add(new Item(description, done, date.toLocalDate()));
            }

            statement.close();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void addItem(Item item) {
        try {
            String sql = "INSERT INTO Item (description, done, date) VALUES (?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.setBoolean(2, item.isDone());
            statement.setDate(3, Date.valueOf(item.getDate()));
            statement.executeUpdate();
            statement.close();
            itemList.add(item); // Add item to the list after successful insertion
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public boolean deleteItem(Item item) {
        try {
            String sql = "DELETE FROM Item WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            int deleted = statement.executeUpdate();
            statement.close();
            if (deleted > 0) {
                itemList.remove(item); // Remove item from list if deleted from database
                return true;
            } else {
                throw new Exception("No se pudo eliminar");
            }
        } catch (Exception e) {
            System.out.println(e.getMessage());
            return false;
        }
    }

    public void finishItem(Item item) {
        try {
            String sql = "UPDATE Item SET done = 1 WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.executeUpdate();
            statement.close();
        } catch (SQLException e) {
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
