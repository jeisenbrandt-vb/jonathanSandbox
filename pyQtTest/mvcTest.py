# model.py
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView, QPushButton, QLineEdit

import sys
from PyQt5.QtWidgets import QApplication
class TodoListModel(QStringListModel):
    def __init__(self):
        super().__init__()

# view.py

# from model import TodoListModel

class TodoListView(QWidget):
    def __init__(self):
        super().__init__()
        self.model = TodoListModel()
        self.list_view = QListView()
        self.list_view.setModel(self.model)

        self.add_button = QPushButton("Add Task")
        self.task_input = QLineEdit()

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_view)
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button)

    def get_new_task(self):
        return self.task_input.text()

# controller.py
# from model import TodoListModel

class TodoListController:
    def __init__(self, view):
        self.view = view
        self.model = TodoListModel()

        self.view.add_button.clicked.connect(self.add_task)

    def add_task(self):
        new_task = self.view.get_new_task()
        self.model.setStringList(self.model.stringList() + [new_task])

# main.py
# from view import TodoListView
# from controller import TodoListController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TodoListView()
    controller = TodoListController(window)
    window.show()
    sys.exit(app.exec_())