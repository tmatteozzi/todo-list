class ToDoListController:
    def __init__(self, view, model):
        self.view = view
        self.model = model
        self.en_menu_principal = True

        self.view.cargar_agregar_item_listener(self.agregar_item)
        self.view.cargar_mostrar_completados_listener(self.mostrar_completados)
        self.view.cargar_salir_listener(self.salir)
        self.view.add_delete_button_listener(self.delete_item)
        self.view.add_finish_button_listener(self.finish_item)

        self.update_view()

    def update_view(self):
        if self.en_menu_principal:
            self.view.update_unfinished(self.model.get_unfinished_items())
        else:
            self.view.update_completed(self.model.get_completed_items())
        self.view.actualizar_nombre_boton_menu(self.en_menu_principal)
        self.view.ocultar_agregar_item(not self.en_menu_principal)

    def agregar_item(self):
        description = self.view.show_input_dialog("Ingrese la descripción del nuevo ítem:")
        if description and description.strip():
            self.model.add_item(Item(description))
            self.update_view()
            self.view.limpiar_textarea()
        else:
            self.view.mostrar_error("El campo de descripción está vacío.")

    def mostrar_completados(self):
        if self.en_menu_principal:
            self.view.update_completed(self.model.get_completed_items())
        else:
            self.view.update_unfinished(self.model.get_unfinished_items())
        self.en_menu_principal = not self.en_menu_principal
        self.update_view()

    def salir(self):
        exit(0)

    def delete_item(self, item_id):
        item_id = int(item_id)
        self.model.delete_item(self.model.get_item(item_id))
        self.update_view()

    def finish_item(self, item_id):
        item_id = int(item_id)
        self.model.finish_item(self.model.get_item(item_id))
        self.update_view()
