
class TodoListController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def add_todo(self, title, description):
        self.model.add_todo(title, description)

    def remove_todo(self, index):
        self.model.remove_todo(index)

    def toggle_complete(self, index):
        self.model.toggle_complete(index)

    def display_todos(self):
        todos = self.model.get_all_todos()
        self.view.show_todos(todos)

    def run(self):
        while True:
            self.display_todos()
            choice = self.view.get_user_choice()

            if choice == '1':
                title = self.view.get_todo_title()
                description = self.view.get_todo_description()
                self.add_todo(title, description)
            elif choice == '2':
                index = self.view.get_todo_index_to_remove()
                self.remove_todo(index)
            elif choice == '3':
                index = self.view.get_todo_index_to_toggle()
                self.toggle_complete(index)
            elif choice == '4':
                break
            else:
                self.view.show_message("Opción inválida. Inténtalo de nuevo.")
