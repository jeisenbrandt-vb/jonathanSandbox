from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
import dl_test_automation

class MainWindow(QMainWindow):
    #create a map where key is combo box name and val is array of items combo box
    #i want to be able to reference the values later in a function call such as
    #auto_dl(combo_boxes[config].current_text(), combo_boxes[].current_text(), combo_boxes[].current_text())
    #this should envolve an list of lists of original inputs, then a map maping the box name to a reference 
    #the box, I'll have to maintain the order which I'm not a super big fan of, but it should work
    def __init__(self):
        super().__init__()
        combo_box_options = [
            list(dl_test_automation.config_paths.keys()),
            [str(i) for i in list(dl_test_automation.ip_addresses.keys())],
            dl_test_automation.deveuis,
            ["VoBoXX", "VoBoTC", "VoBoXP"],
            ["1.00.00","2.00.00","2.01.00"],
            ["Downlinks", "OutOfRange", "MinRange", "MaxRange"],
            ["A", "C"],
            ["True", "False"],
        ]
        self.combo_boxes = {
            "config":           None,
            "gateway_ip":       None,
            "deveui":           None,
            "vobo_type":        None,
            "vobo_version":     None,
            "test_type":        None,
            "lorawan_class":    None,
            "cont_meas":        None,
        }

        self.setWindowTitle("LoRa Net Hub")
        self.setGeometry(100, 100, 400, 250)

        # Set up the central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        i = 0
        for key in self.combo_boxes:
            label = QLabel(key)
            combo_box = QComboBox()
            combo_box.addItems(combo_box_options[i])
            self.combo_boxes[key] = combo_box
            layout.addWidget(label)
            layout.addWidget(combo_box)
            i += 1
        
        start_test_button = QPushButton("Start Test")
        layout.addWidget(start_test_button)

        self.setCentralWidget(central_widget)

    # def on_combobox_changed(self):
    #     selected_item = dl_test_automation.config_paths[self.config_selector.currentText()]
    #     self.label.setText(f"Selected: {selected_item}")
    def run_test(self):
        pass

    def apply_dark_mode_styles(self):
        """ Apply dark mode styling to the app """
        self.setStyleSheet("""
            /* Dark Mode Styling */
            QMainWindow {
                background-color: #121212;  /* Dark background */
                color: #f1f1f1;  /* Light text color */
            }

            /* Title label */
            #titleLabel {
                font-size: 18px;
                font-weight: bold;
                color: #f1f1f1;
                margin-bottom: 10px;
            }

            /* Input field */
            #inputField {
                background-color: #333;  /* Dark input field */
                border: 2px solid #555;  /* Soft border */
                color: #f1f1f1;  /* Light text in the input field */
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }

            #inputField:focus {
                border-color: #6200ea;  /* Purple border on focus */
                box-shadow: 0 0 5px rgba(98, 0, 234, 0.5);  /* Purple glow */
            }

            /* Button */
            #actionButton {
                background-color: #6200ea;  /* Purple button */
                color: white;
                font-size: 14px;
                border: none;
                padding: 10px;
                border-radius: 5px;
                margin-top: 15px;
                cursor: pointer;
            }

            #actionButton:hover {
                background-color: #3700b3;  /* Darker purple on hover */
            }

            #actionButton:pressed {
                background-color: #6200ea;  /* Purple on button press */
            }

            /* Output label */
            #outputLabel {
                font-size: 14px;
                color: #f1f1f1;  /* Light text for output */
                margin-top: 20px;
                font-style: italic;
            }

            /* Placeholder text in input field */
            QLineEdit::placeholder {
                color: #888;  /* Lighter placeholder text */
            }
        """)

    def get_input_text(self):
        return self.input_field.text()

    def set_output_text(self, text):
        self.output_label.setText(text)
