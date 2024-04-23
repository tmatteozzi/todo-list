from sqlalchemy import Column, Integer, String, Boolean

from ModeloMVC_py.config import Base


class TodoItem(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255))
    completed = Column(Boolean, default=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.completed = False
