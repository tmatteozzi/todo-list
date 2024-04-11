# todoListController.py
from pubsub import pub
from item import Item


class ToDoListController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.en_menu_principal = True

        pub.subscribe(self.agregar_item, "add_item")
        pub.subscribe(self.mostrar_completados, "mostrar_completados")
        pub.subscribe(self.salir, "salir")
        pub.subscribe(self.finish_item, "finish_item")
        pub.subscribe(self.delete_item, "delete_item")
        pub.subscribe(self.update_unfinished_items, "request_unfinished_items")
        pub.subscribe(self.update_completed_items, "request_completed_items")

    def agregar_item(self, description):
        self.model.add_item(Item(description))
        self.update_view()

    def mostrar_completados(self):
        self.en_menu_principal = not self.en_menu_principal
        self.update_view()

    def update_view(self):
        if self.en_menu_principal:
            unfinished_items = self.model.get_unfinished_items()
            self.view.update_unfinished(unfinished_items)
        else:
            completed_items = self.model.get_completed_items()
            self.view.update_unfinished(completed_items)  # Aquí actualizamos con los completados
        self.view.actualizar_nombre_boton_menu(self.en_menu_principal)
        self.view.ocultar_agregar_item(not self.en_menu_principal)

    def salir(self):
        exit(0)

    def delete_item(self, item_id):
        self.model.delete_item(self.model.get_item(int(item_id)))
        self.update_view()

    def finish_item(self, item_id):
        self.model.finish_item(self.model.get_item(int(item_id)))
        self.update_view()

    def update_unfinished_items(self):
        self.update_view()  # No necesitamos obtener los elementos no finalizados aquí

    def update_completed_items(self):
        self.update_view()  # No necesitamos obtener los elementos completados aquí
