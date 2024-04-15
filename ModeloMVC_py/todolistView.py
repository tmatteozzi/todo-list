
class TodoListView:
    def show_todos(self, todos):
        if todos:
            print("Lista de tareas:")
            for index, todo in enumerate(todos):
                print(f"{index + 1}. {todo}")
        else:
            print("No hay tareas en la lista.")

    def get_user_choice(self):
        print("\nMenú:")
        print("1. Agregar tarea")
        print("2. Eliminar tarea")
        print("3. Marcar tarea como completada/pendiente")
        print("4. Salir")
        return input("Selecciona una opción: ")

    def get_todo_title(self):
        return input("Ingrese el título de la tarea: ")

    def get_todo_description(self):
        return input("Ingrese la descripción de la tarea: ")

    def get_todo_index_to_remove(self):
        return int(input("Ingrese el número de la tarea que desea eliminar: ")) - 1

    def get_todo_index_to_toggle(self):
        return int(input("Ingrese el número de la tarea que desea marcar como completada/pendiente: ")) - 1

    def show_message(self, message):
        print(message)
