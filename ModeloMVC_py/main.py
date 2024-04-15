#Modelo MVC Ing de stofware 2
#Verion 0.0.1

from ModeloMVC_py.todolistModel import TodoListModel
from ModeloMVC_py.todolistView import TodoListView
from ModeloMVC_py.todolistController import TodoListController


def main():
    model = TodoListModel()
    view = TodoListView(model)
    controller = TodoListController(model, view)

    view.mainloop()

if __name__ == "__main__":
    main()
