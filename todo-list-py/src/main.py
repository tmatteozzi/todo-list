from todoListModel import ToDoListModel
from todoListView import ToDoListView
from todoListController import ToDoListController

if __name__ == "__main__":
    # Crear instancias del modelo, vista y controlador
    model = ToDoListModel()
    view = ToDoListView()
    controller = ToDoListController(view, model)

    # Iniciar la interfaz gráfica
    view.mainloop()
