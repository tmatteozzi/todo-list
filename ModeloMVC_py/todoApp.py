
import tkinter as tk
from tkinter import messagebox

from ModeloMVC_py.todolistController import TodoListController
from ModeloMVC_py.todolistModel import TodoListModel
from ModeloMVC_py.todolistView import TodoListView

import tkinter as tk
from tkinter import simpledialog, messagebox

class Interfaz(tk.Tk):
    def __init__(self, model, controller):
        super().__init__()
        self.title("Lista de Tareas")
        self.model = model
        self.controller = controller

        self.create_widgets()

    def create_widgets(self):
        self.todo_listbox = tk.Listbox(self, width=50, height=15)
        self.todo_listbox.pack(pady=10)

        self.add_button = tk.Button(self, text="Agregar Tarea", command=self.add_todo)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(self, text="Eliminar Tarea", command=self.remove_todo)
        self.remove_button.pack(pady=5)

        self.complete_button = tk.Button(self, text="Marcar como Completada", command=self.toggle_complete)
        self.complete_button.pack(pady=5)

        self.exit_button = tk.Button(self, text="Salir", command=self.quit)
        self.exit_button.pack(pady=5)

    def add_todo(self):
        title = self.ask_user_input("Título de la Tarea")
        if title:
            description = self.ask_user_input("Descripción de la Tarea")
            self.controller.add_todo(title, description)
            self.refresh_list()

    def remove_todo(self):
        index = self.todo_listbox.curselection()
        if index:
            index = int(index[0])
            self.controller.remove_todo(index)
            self.refresh_list()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar.")

    def toggle_complete(self):
        index = self.todo_listbox.curselection()
        if index:
            index = int(index[0])
            self.controller.toggle_complete(index)
            self.refresh_list()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar como completada.")

    def refresh_list(self):
        self.todo_listbox.delete(0, tk.END)
        todos = self.model.get_all_todos()
        for index, todo in enumerate(todos):
            status = "Completada" if todo.completed else "Pendiente"
            self.todo_listbox.insert(tk.END, f"{todo.title} - {todo.description} ({status})")

    def ask_user_input(self, title):
        return simpledialog.askstring(title, f"Ingrese {title.lower()} de la tarea:")

def main():
    model = TodoListModel()
    view = TodoListView()
    controller = TodoListController(model, view)

    app = Interfaz(model, controller)
    app.mainloop()

if __name__ == "__main__":
    main()

