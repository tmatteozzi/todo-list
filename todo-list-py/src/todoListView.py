import tkinter as tk
from tkinter import messagebox, simpledialog


class ToDoListView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TO DO LIST")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.button_panel = tk.Frame(self)
        self.button_panel.pack(side="top")

        self.add_item_button = tk.Button(self.button_panel, text="AGREGAR ITEM")
        self.add_item_button.pack(side="left")

        self.menu_button = tk.Button(self.button_panel, text="COMPLETADOS")
        self.menu_button.pack(side="left")

        self.exit_button = tk.Button(self.button_panel, text="SALIR", command=self.salir)
        self.exit_button.pack(side="left")

        self.item_panel = tk.Frame(self)
        self.item_panel.pack(side="top", fill="both", expand=True)

        self.text_area = tk.Text(self.item_panel, height=5, width=20)
        self.text_area.pack(side="bottom")

        self.delete_buttons = []
        self.finish_buttons = []

    def update_unfinished(self, item_list):
        self.clear_item_panel()
        for item in item_list:
            self.create_item_widget(item)

    def update_completed(self, item_list):
        self.clear_item_panel()
        for item in item_list:
            self.create_item_widget(item)

    def clear_item_panel(self):
        for widget in self.item_panel.winfo_children():
            widget.destroy()

    def create_item_widget(self, item):
        item_row = tk.Frame(self.item_panel)
        item_row.pack(fill="x")

        item_label = tk.Label(item_row, text=item.description)
        item_label.pack(side="left")

        button_panel = tk.Frame(item_row)
        button_panel.pack(side="right")

        finish_button = tk.Button(button_panel, text="FINALIZAR",
                                  command=lambda id=item.id: self.finish_item(id))
        finish_button.pack(side="left")
        self.finish_buttons.append(finish_button)

        delete_button = tk.Button(button_panel, text="ELIMINAR",
                                  command=lambda id=item.id: self.delete_item(id))
        delete_button.pack(side="left")
        self.delete_buttons.append(delete_button)

    def show_input_dialog(self, message):
        return simpledialog.askstring("Input", message)

    def limpiar_textarea(self):
        self.text_area.delete(1.0, tk.END)

    def mostrar_error(self, mensaje_error):
        messagebox.showerror("Error", mensaje_error)

    def cargar_agregar_item_listener(self, on_add_item_callback):
        self.add_item_button["command"] = on_add_item_callback

    def cargar_mostrar_completados_listener(self, on_show_completed_callback):
        self.menu_button["command"] = on_show_completed_callback

    def cargar_salir_listener(self, on_exit_callback):
        self.exit_button["command"] = on_exit_callback

    def add_delete_button_listener(self, on_delete_item_callback):
        for button in self.delete_buttons:
            button["command"] = lambda id=button.id: on_delete_item_callback(id)

    def add_finish_button_listener(self, on_finish_item_callback):
        for button in self.finish_buttons:
            button["command"] = lambda id=button.id: on_finish_item_callback(id)

    def actualizar_nombre_boton_menu(self, en_menu_principal):
        if en_menu_principal:
            self.menu_button["text"] = "COMPLETADOS"
        else:
            self.menu_button["text"] = "SIN TERMINAR"

    def ocultar_agregar_item(self, ocultar):
        if ocultar:
            self.add_item_button.pack_forget()
        else:
            self.add_item_button.pack(side="left")

    def salir(self):
        exit(0)
