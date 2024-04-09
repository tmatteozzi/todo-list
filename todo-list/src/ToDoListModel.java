import java.util.ArrayList;

public class ToDoListModel {
    private ArrayList<Item> itemList;

    public ToDoListModel() {
        itemList = new ArrayList<>();
        new DbBroker();
        getAllItems();
    }

    // MÉTODOS DE LA DB
    public void getAllItems(){
        try {
            itemList = DbBroker.getAllItems();
        } catch (Exception e){
            System.out.println(e.getMessage());
        }
    }

    public void addItem(Item item) {
        try {
            DbBroker.addItem(item);
            itemList.add(item);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public void deleteItem(Item item) {
        try {
            boolean deleted = DbBroker.deleteItem(item);
            if (deleted) {
                itemList.remove(item);
            } else {
                throw new Exception("Error al eliminar el ítem de la base de datos.");
            }
        } catch (Exception e) {
            System.out.println("Error al eliminar el ítem: " + e.getMessage());
        }
    }
    

    public void finishItem(Item item) {
        try {
            DbBroker.finishItem(item);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    // METODOS ARRAYLIST
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
