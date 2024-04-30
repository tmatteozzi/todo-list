from todolistController import TodoListController
from todolistModel import TodoListModel
from todolistView import TodoListView

if __name__ == "__main__":
    model = TodoListModel()
    view = TodoListView()
    controller = TodoListController(view, model)
    view.mainloop()
