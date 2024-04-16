class TodoListController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # Configurar callbacks
        self.view.set_add_todo_callback(self.add_todo)
        self.view.set_remove_todo_callback(self.remove_todo)
        self.view.set_toggle_complete_callback(self.toggle_complete)

        # Agregar vista como observador
        self.model.add_observer(self.view)

    def add_todo(self):
        title = self.view.ask_user_input("Título de la Tarea")
        if title:
            description = self.view.ask_user_input("Descripción de la Tarea")
            self.model.add_todo(title, description)

    def remove_todo(self):
        index = self.view.todo_listbox.curselection()
        if index:
            index = int(index[0])
            self.model.remove_todo(index)

    def toggle_complete(self):
        index = self.view.todo_listbox.curselection()
        if index:
            index = int(index[0])
            self.model.toggle_complete(index)
