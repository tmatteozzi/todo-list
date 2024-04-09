import java.sql.*;
import java.util.ArrayList;

public class DbBroker {
    private static final String DB_URL = "jdbc:sqlite:/Users/tomasmatteozzi/Documents/workspaces/uni/ingenieria-de-software-2/todo-list/todo-list/src/todolist.db";
    private static Connection connection = null;

    public DbBroker(){
        try {
            Class.forName("org.sqlite.JDBC");
            connection = DriverManager.getConnection(DB_URL);
            System.out.println("Conexión exitosa a la BD.");
        } catch (ClassNotFoundException | SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    static ArrayList<Item> getAllItems(){
        ArrayList<Item> itemList = new ArrayList<>();
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
            return itemList;
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return null;
        }
    }

    static void addItem(Item item) {
        try {
            String sql = "INSERT INTO Item (description, done, date) VALUES (?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.setBoolean(2, item.isDone());
            statement.setDate(3, Date.valueOf(item.getDate()));
            statement.executeUpdate();
            statement.close();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    static boolean deleteItem(Item item) {
        try {
            String sql = "DELETE FROM Item WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            int deleted = statement.executeUpdate();
            statement.close();
            if (deleted > 0) {
                return true;
            } else {
                throw new SQLException("No se pudo eliminar");
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
            return false;
        }
    }

    static void finishItem(Item item) {
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
}
