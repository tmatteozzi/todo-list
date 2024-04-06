import java.sql.*;
import java.util.ArrayList;

public class ToDoListModel {
    private static final String DB_URL = "jdbc:sqlite:/Users/tomasmatteozzi/Documents/workspaces/uni/ingenieria-de-software-2/todo-list/todo-list/src/todolist.db";
    private Connection connection = null;
    private ArrayList<Item> itemList;

    public ToDoListModel() {
        itemList = new ArrayList<>();
        try {
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection(DB_URL);
            System.out.println("Conexión exitosa a la BD.");
            loadItemsFromDatabase();
        } catch (ClassNotFoundException | SQLException e) {
            handleException(e);
        }
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
            handleException(e);
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
            itemList.add(item);
        } catch (SQLException e) {
            handleException(e);
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
                itemList.remove(item);
                return true;
            } else {
                throw new SQLException("No se pudo eliminar");
            }
        } catch (SQLException e) {
            handleException(e);
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
            handleException(e);
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

    private void handleException(Exception e) {
        e.printStackTrace();
        // Aquí puedes agregar código para manejar la excepción de manera adecuada, por ejemplo, mostrar un mensaje de error al usuario.
    }
}
