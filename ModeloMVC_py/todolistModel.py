from dbBroker import dbBroker

class TodoListModel:
    def __init__(self):
        # Crear una instancia de dbBroker para poder acceder a sus métodos
        self.db_broker = dbBroker()

    def add_todo(self, title, description):
        # Llamar al método add_todo de dbBroker a través de la instancia
        self.db_broker.add_todo(title, description)

    def remove_todo(self, id):
        # Llamar al método remove_todo de dbBroker a través de la instancia
        self.db_broker.remove_todo(id)

    def toggle_complete(self, id):
        # Llamar al método toggle_complete de dbBroker a través de la instancia
        self.db_broker.toggle_complete(id)

    def get_all_todos(self):
        # Llamar al método get_all_todos de dbBroker a través de la instancia
        return self.db_broker.get_all_todos()

    def get_todo_by_id(self, id):
        # Llamar al método get_todo_by_id de dbBroker a través de la instancia
        return self.db_broker.get_todo_by_id(id)
