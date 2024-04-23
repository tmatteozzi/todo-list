from dbBroker import dbBroker

class TodoListModel:
    def __init__(self):
        self.db_broker = dbBroker()

    def add_todo(self, title, description):
        self.db_broker.add_todo(title, description)

    def edit_todo(self, id, new_title, new_description):
        return self.db_broker.edit_todo(id, new_title, new_description)

    def remove_todo(self, id):
        self.db_broker.remove_todo(id)

    def toggle_complete(self, id):
        self.db_broker.toggle_complete(id)

    def get_all_todos(self):
        return self.db_broker.get_all_todos()

    def get_todo_by_id(self, id): \
            return self.db_broker.get_todo_by_id(id)
