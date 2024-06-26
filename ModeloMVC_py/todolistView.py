import tkinter as tk
from tkinter import simpledialog

class TodoListView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lista de Tareas")
        self.completed_label = tk.Label(self, text="0/0 items completados")
        self.completed_label.pack(pady=5)
        self.create_widgets()

        self.task_map = {}  # DICCIONARIO PARA ASOCIAR IDs DE CADA ITEM

    def set_add_todo_callback(self, callback):
        self.add_todo_callback = callback

    def set_remove_todo_callback(self, callback):
        self.remove_todo_callback = callback

    def set_toggle_complete_callback(self, callback):
        self.toggle_complete_callback = callback

    def set_show_details_callback(self, callback):
        self.show_details_callback = callback

    def set_edit_todo_callback(self, callback):
        self.edit_todo_callback = callback

    def create_widgets(self):
        self.todo_listbox = tk.Listbox(self, width=50, height=15)
        self.todo_listbox.pack(pady=10)
        self.add_button = tk.Button(self, text="Agregar Tarea", command=self.add_todo)
        self.add_button.pack(pady=5)
        self.edit_button = tk.Button(self, text="Editar Tarea", command=self.edit_todo)
        self.edit_button.pack(pady=5)
        self.remove_button = tk.Button(self, text="Eliminar Tarea", command=self.remove_todo)
        self.remove_button.pack(pady=5)
        self.complete_button = tk.Button(self, text="Marcar como Completada", command=self.toggle_complete)
        self.complete_button.pack(pady=5)
        self.show_details_button = tk.Button(self, text="+ Info", command=self.show_details)
        self.show_details_button.pack(pady=5)
        self.exit_button = tk.Button(self, text="Salir", command=self.quit)
        self.exit_button.pack(pady=5)

    def add_todo(self):
        if hasattr(self, 'add_todo_callback'):
            self.add_todo_callback()

    def edit_todo(self):
        if hasattr(self, 'edit_todo_callback'):
            self.edit_todo_callback()

    def remove_todo(self):
        if hasattr(self, 'remove_todo_callback'):
            self.remove_todo_callback()

    def toggle_complete(self):
        if hasattr(self, 'toggle_complete_callback'):
            self.toggle_complete_callback()

    def show_details(self):
        if hasattr(self, 'show_details_callback'):
            self.show_details_callback()

    def update(self, todos):
        self.todo_listbox.delete(0, tk.END)
        self.task_map.clear()  # VACIAR DICCIONARIO
        for todo in todos:
            status = "Completada" if todo.completed else "Pendiente"
            item = f"{todo.title} - ({status})"
            self.todo_listbox.insert(tk.END, item)
            task_id = self.todo_listbox.index(tk.END) - 1  # OBTENER INDICE DEL ELEMENTO
            self.task_map[task_id] = todo.id  # HACER QUE EL INDICE SEA EL ID

    def update_completed_label(self, completed_count, total_count):
        self.completed_label.config(text=f"{completed_count}/{total_count} items completados")

    def ask_user_input(self, title):
        data = simpledialog.askstring(title, f"Ingrese {title.lower()}:")
        while (data == ''):
            simpledialog.messagebox.showerror("Error", "Este campo no puede estar vacío.")
            data = simpledialog.askstring(title, f"Ingrese {title.lower()}:")
        return data

    def show_info_panel(self, title, description, status):
        self.info_panel = tk.Toplevel(self)
        self.info_panel.title("Detalles de la Tarea")

        info_label = tk.Label(self.info_panel, text=f"Título: \n{title}\nDescripción: \n{description}\nEstado: {status}")
        info_label.pack(padx=10, pady=10)

        close_button = tk.Button(self.info_panel, text="Cerrar", command=self.close_info_panel)
        close_button.pack(pady=5)

    def close_info_panel(self):
        if hasattr(self, 'info_panel'):
            self.info_panel.destroy()
