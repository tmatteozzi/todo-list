import java.util.ArrayList;

public class ToDoListModel {
    private ArrayList<Item> itemList;

    public ToDoListModel() {
        itemList = new ArrayList<>();
        new DbBroker();
        getAllItems();
        System.out.println();
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
            DbBroker.deleteItem(item);
            if (true) {
                itemList.remove(item);
            } 
        } catch (Exception e) {
            System.out.println(e.getMessage());
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
