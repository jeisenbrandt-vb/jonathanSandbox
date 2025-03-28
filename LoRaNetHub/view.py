# view.py
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My PyQt App")
        self.setGeometry(100, 100, 400, 200)

        # Create UI components
        self.label = QLabel("Enter something:")
        self.input_field = QLineEdit()
        self.button = QPushButton("Process")
        self.output_label = QLabel("")

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_input_text(self):
        return self.input_field.text()

    def set_output_text(self, text):
        self.output_label.setText(text)
