# controller.py
from model import MyAppLogic
from view import MainWindow

class Controller:
    def __init__(self, view: MainWindow, model: MyAppLogic):
        self.view = view
        self.model = model

        # Connect the button click to the controller method
        # self.view.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        user_input = self.view.get_input_text()
        result = self.model.process_input(user_input)
        self.view.set_output_text(result)
