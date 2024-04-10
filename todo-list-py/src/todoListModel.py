from dbBroker import DbBroker
from item import Item


class ToDoListModel:
    def __init__(self):
        self.item_list = []
        DbBroker()
        self.get_all_items()
        print(self.item_list)

    # Métodos de la base de datos
    def get_all_items(self):
        try:
            self.item_list = DbBroker.get_all_items()
        except Exception as e:
            print(e)

    def add_item(self, item):
        try:
            DbBroker.add_item(item)
            self.item_list.append(item)
        except Exception as e:
            print(e)

    def delete_item(self, item):
        try:
            deleted = DbBroker.delete_item(item)
            if deleted:
                self.item_list.remove(item)
            else:
                raise Exception("Error al eliminar el ítem de la base de datos.")
        except Exception as e:
            print("Error al eliminar el ítem: " + str(e))

    def finish_item(self, item):
        try:
            DbBroker.finish_item(item)
        except Exception as e:
            print(e)

    def get_item(self, id):
        try:
            return DbBroker.get_item(id)
        except Exception as e:
            print(e)
            return None

    # Métodos ArrayList
    def get_unfinished_items(self):
        unfinished_items = []
        for item_data in self.item_list:
            if not item_data.done:
                item = Item(item_data.id, item_data.description, item_data.date, item_data.done)
                unfinished_items.append(item)
        return unfinished_items

    def get_completed_items(self):
        completed_items = []
        for item_data in self.item_list:
            if item_data.done:
                item = Item(item_data.id, item_data.description, item_data.date, item_data.done)
                completed_items.append(item)
        return completed_items
