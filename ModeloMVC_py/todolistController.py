class TodoListController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.view.set_add_todo_callback(self.add_todo)
        self.view.set_edit_todo_callback(self.edit_todo)
        self.view.set_remove_todo_callback(self.remove_todo)
        self.view.set_toggle_complete_callback(self.toggle_complete)
        self.view.set_show_details_callback(self.show_details)
        self.update_view()

    def add_todo(self):
        title = self.view.ask_user_input("Título de la Tarea")
        if title:
            description = self.view.ask_user_input("Descripción de la Tarea")
            self.model.add_todo(title, description)
            self.update_view()

    def edit_todo(self):
        index = self.view.todo_listbox.curselection()
        if index:
            task_id = self.view.task_map.get(index[0])  # OBTENER EL ID DESDE EL DICCIONARIO
            if task_id is not None:
                self.edit_todo_dialog(task_id)

    def edit_todo_dialog(self, todo_id):
        new_title = self.view.ask_user_input("Nuevo Título de la Tarea")
        if new_title:
            new_description = self.view.ask_user_input("Nueva Descripción de la Tarea")
            if new_description:
                self.model.edit_todo(todo_id, new_title, new_description)
                self.update_view()

    def remove_todo(self):
        index = self.view.todo_listbox.curselection()
        if index:
            task_id = self.view.task_map.get(index[0])  # OBTENER EL ID DESDE EL DICCIONARIO
            if task_id is not None:
                self.model.remove_todo(task_id)
                self.update_view()

    def toggle_complete(self):
        index = self.view.todo_listbox.curselection()
        if index:
            task_id = self.view.task_map.get(index[0])  # OBTENER EL ID DESDE EL DICCIONARIO
            if task_id is not None:
                self.model.toggle_complete(task_id)
                self.update_view()

    def show_details(self):
        index = self.view.todo_listbox.curselection()
        if index:
            task_id = self.view.task_map.get(index[0])  # OBTENER EL ID DESDE EL DICCIONARIO
            if task_id is not None:
                todo = self.model.get_todo_by_id(task_id)
                status = "Completada" if todo.completed else "Pendiente"
                self.view.show_info_panel(todo.title, todo.description, status)

    def update_view(self):
        todos = self.model.get_all_todos()
        completed_count = sum(1 for todo in todos if todo.completed)
        total_count = len(todos)
        self.view.update_completed_label(completed_count, total_count)
        self.view.update(todos)
