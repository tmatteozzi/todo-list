from todoItem import TodoItem

class TodoListModel:
    def __init__(self):
        self.todo_list = []
        self.observers = []

    # METODOS DE OBSERVERS
    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.todo_list)

    # METODOS DE MODIFICACION DE LA TODOLIST
    def add_todo(self, title, description):
        new_todo = TodoItem(title, description)
        self.todo_list.append(new_todo)
        self.notify_observers()

    def remove_todo(self, index):
        if 0 <= index < len(self.todo_list):
            del self.todo_list[index]
            self.notify_observers()

    def toggle_complete(self, index):
        if 0 <= index < len(self.todo_list):
            self.todo_list[index].completed = not self.todo_list[index].completed
            self.notify_observers()

    def get_all_todos(self):
        return self.todo_list
