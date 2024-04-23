from sqlalchemy.orm import sessionmaker
from todoItem import TodoItem

from config import engine

Session = sessionmaker(bind=engine)

class dbBroker:
    def add_todo(self, title, description):
        session = Session()
        new_todo = TodoItem(title, description)
        session.add(new_todo)
        session.commit()

    def remove_todo(self, id):
        session = Session()
        todo = session.query(TodoItem).filter_by(id=id).first()
        if todo:
            session.delete(todo)
            session.commit()

    def toggle_complete(self, id):
        session = Session()
        todo = session.query(TodoItem).filter_by(id=id).first()
        if todo:
            todo.completed = not todo.completed
            session.commit()

    def get_all_todos(self):
        session = Session()
        return session.query(TodoItem).all()

    def get_todo_by_id(self, id):
        session = Session()
        return session.query(TodoItem).filter_by(id=id).first()