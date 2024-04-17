class TodoItem:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False

    def __str__(self):
        status = "Completada" if self.completed else "Pendiente"
        return f"{self.title} - ({status})"