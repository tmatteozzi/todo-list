from ModeloMVC_py.todoItem import TodoItem

class TodoListModel:
    def __init__(self):
        self.todo_list = []

    def add_todo(self, title, description):
        new_todo = TodoItem(title, description)
        self.todo_list.append(new_todo)

    def remove_todo(self, index):
        if 0 <= index < len(self.todo_list):
            del self.todo_list[index]
        else:
            print("Índice fuera de rango")

    def toggle_complete(self, index):
        if 0 <= index < len(self.todo_list):
            self.todo_list[index].completed = not self.todo_list[index].completed
        else:
            print("Índice fuera de rango")

    def get_all_todos(self):
        return self.todo_list


