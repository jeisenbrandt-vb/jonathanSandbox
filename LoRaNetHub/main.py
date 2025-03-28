# main.py
import sys
from PyQt5.QtWidgets import QApplication
from model import MyAppLogic
from view import MainWindow
from controller import Controller

def main():
    app = QApplication(sys.argv)

    # Create model, view, and controller
    model = MyAppLogic()
    view = MainWindow()
    controller = Controller(view, model)

    # Show the window
    view.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
