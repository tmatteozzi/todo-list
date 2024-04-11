import tkinter as tk
from tkinter import messagebox, simpledialog
from pubsub import pub


class ToDoListView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TO DO LIST")
        self.geometry("800x600")
        self.en_menu_principal = True
        self.menu_principal()

    def menu_principal(self):
        self.clear_all_widgets()

        # CREAR BOTONES
        self.add_item_button = tk.Button(self, text="AGREGAR ITEM", command=self.add_item)
        self.add_item_button.pack(side="top")

        self.completados_button = tk.Button(self, text="COMPLETADOS", command=self.mostrar_completados)
        self.completados_button.pack(side="top")

        self.exit_button = tk.Button(self, text="SALIR", command=self.salir)
        self.exit_button.pack(side="top")

        # CREAR ITEM PANEL
        self.item_panel = tk.Frame(self)
        self.item_panel.pack(side="top", fill="both", expand=True)

        # MOSTRAR Y ACTUALIZAR LOS ITEMS NO COMPLETADOS
        self.update_unfinished()

    def mostrar_completados(self):
        if self.en_menu_principal:
            self.completados_button.config(text="SIN TERMINAR", command=self.menu_principal)
            self.add_item_button.pack_forget()
            pub.sendMessage("request_completed_items")
            self.en_menu_principal = False
        else:
            self.menu_principal()

    def update_unfinished(self):
        self.clear_item_panel()
        # Aquí deberías tener algún mecanismo para obtener los elementos no finalizados
        unfinished_items = []  # Por ahora, mantenemos la lista vacía
        for item in unfinished_items:
            self.create_item_widget(item)

    def create_item_widget(self, item):
        # CREAR FILA DE ITEM
        item_row = tk.Frame(self.item_panel)
        item_row.pack(fill="x")

        # DESCRIPCION DEL ITEM
        item_label = tk.Label(item_row, text=item.get_description())
        item_label.pack(side="left")

        # CREAR BOTONES DEL ITEM
        button_panel = tk.Frame(item_row)
        button_panel.pack(side="right")

        delete_button = tk.Button(button_panel, text="ELIMINAR",
                                  command=lambda id=item.get_id(): pub.sendMessage("delete_item", item_id=id))
        delete_button.pack(side="left")

        finish_button = tk.Button(button_panel, text="FINALIZAR",
                                  command=lambda id=item.get_id(): pub.sendMessage("finish_item", item_id=id))
        finish_button.pack(side="left")

    def add_item(self):
        description = self.show_input_dialog("Ingrese la descripción del nuevo ítem:")
        if description and description.strip():
            pub.sendMessage("add_item", description=description)
        else:
            self.mostrar_error("El campo de descripción está vacío.")

    def salir(self):
        exit(0)

    # MÉTODOS AUXILIARES
    def clear_all_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

    def clear_item_panel(self):
        for widget in self.item_panel.winfo_children():
            widget.destroy()

    def show_input_dialog(self, message):
        return simpledialog.askstring("Input", message)

    def mostrar_error(self, mensaje_error):
        messagebox.showerror("Error", mensaje_error)
