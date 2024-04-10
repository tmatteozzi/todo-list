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

    static ArrayList<Item> getAllItems() throws SQLException{
        ArrayList<Item> itemList = new ArrayList<>();
        try {
            String sql = "SELECT * FROM Item";
            Statement statement = connection.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);

            while (resultSet.next()) {
                int id = resultSet.getInt("id");
                String description = resultSet.getString("description");
                boolean done = resultSet.getBoolean("done");
                Date date = resultSet.getDate("date");
                itemList.add(new Item(id, description, done, date.toLocalDate()));
            }
            statement.close();
            return itemList;
        } catch (SQLException e) {
            throw new SQLException("Error al obtener todos los ítems: " + e.getMessage());
        }
    }

    static void addItem(Item item) throws SQLException {
        try {
            String sql = "INSERT INTO Item (description, done, date) VALUES (?, ?, ?)";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.setBoolean(2, item.isDone());
            statement.setDate(3, Date.valueOf(item.getDate()));
            statement.executeUpdate();
            statement.close();
        } catch (SQLException e) {
            throw new SQLException("Error al agregar un ítem: " + e.getMessage());
        }
    }

    static boolean deleteItem(Item item) throws SQLException {
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
            throw new SQLException("Error al eliminar un ítem: " + e.getMessage());
        }
    }

    static void finishItem(Item item) throws SQLException {
        try {
            String sql = "UPDATE Item SET done = 1 WHERE description = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setString(1, item.getDescription());
            statement.executeUpdate();
            statement.close();
        } catch (SQLException e) {
            throw new SQLException("Error al finalizar un ítem: " + e.getMessage());
        }
    }

    static Item getItem(int id) throws SQLException {
        try {
            String sql = "SELECT * FROM Item WHERE id = ?";
            PreparedStatement statement = connection.prepareStatement(sql);
            statement.setInt(1, id);
            ResultSet resultSet = statement.executeQuery();

            if (resultSet.next()) {
                String description = resultSet.getString("description");
                boolean done = resultSet.getBoolean("done");
                Date date = resultSet.getDate("date");
                // Assuming your Item class has a constructor that accepts these parameters
                return new Item(id, description, done, date.toLocalDate());
            } else {
                throw new SQLException("No item found with ID: " + id);
            }
        } catch (SQLException e) {
            throw new SQLException("Error retrieving item by ID: " + e.getMessage());
        }
    }

}
