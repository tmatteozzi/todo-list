public class Main {
    public static void main(String[] args) {
        ToDoListModel model = new ToDoListModel();
        ToDoListView view = new ToDoListView(model);
        @SuppressWarnings("unused")
        ToDoListController controller = new ToDoListController(view, model);
    }
}
