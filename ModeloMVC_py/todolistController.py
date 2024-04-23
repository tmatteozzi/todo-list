import re
class TodoListController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        # CALLBACKS
        self.view.set_add_todo_callback(self.add_todo)
        self.view.set_edit_todo_callback(self.edit_todo)
        self.view.set_remove_todo_callback(self.remove_todo)
        self.view.set_toggle_complete_callback(self.toggle_complete)
        self.view.set_show_details_callback(self.show_details)
        self.update_view()

    # METODOS
    def add_todo(self):
        title = self.view.ask_user_input("Título de la Tarea")
        if title:
            description = self.view.ask_user_input("Descripción de la Tarea")
            self.model.add_todo(title, description)
            self.update_view()

    def edit_todo(self):
        index = self.view.todo_listbox.curselection()
        if index:
            item_selected = [self.view.todo_listbox.get(i) for i in index]
            if item_selected:
                id_item_selected = re.search(r'\[(.*?)]', item_selected[0])
                self.edit_todo_dialog(id_item_selected.group(1))

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
            item_selected = [self.view.todo_listbox.get(i) for i in index]
            if item_selected:
                id_item_selected = re.search(r'\[(.*?)\]', item_selected[0])
                self.model.remove_todo(id_item_selected.group(1))
                self.update_view()

    def toggle_complete(self):
        index = self.view.todo_listbox.curselection()
        if index:
            item_selected = [self.view.todo_listbox.get(i) for i in index]
            if item_selected:
                id_item_selected = re.search(r'\[(.*?)\]', item_selected[0])
                self.model.toggle_complete(id_item_selected.group(1))
                self.update_view()

    def show_details(self):
        index = self.view.todo_listbox.curselection()
        if index:
            item_selected = [self.view.todo_listbox.get(i) for i in index]
            if item_selected:
                id_item_selected = re.search(r'\[(.*?)\]', item_selected[0])
                todo = self.model.get_todo_by_id(id_item_selected.group(1))
                status = "Completada" if todo.completed else "Pendiente"
                self.view.show_info_panel(todo.title, todo.description, status)

    def update_view(self):
        todos = self.model.get_all_todos()
        self.view.update(todos)
