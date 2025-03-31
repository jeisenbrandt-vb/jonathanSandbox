from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Modern Dark Mode PyQt App")
        self.setGeometry(100, 100, 400, 250)

        # Set up the central widget and layout
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)

        # Title Label
        self.label = QLabel("Enter something:")
        self.label.setObjectName("titleLabel")

        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type here...")
        self.input_field.setObjectName("inputField")

        # Button
        self.button = QPushButton("Process")
        self.button.setObjectName("actionButton")

        # Output Label
        self.output_label = QLabel("")
        self.output_label.setObjectName("outputLabel")

        # Add widgets to layout
        layout.addWidget(self.label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)

        # Set the central widget
        self.setCentralWidget(central_widget)

        # Apply dark mode style
        self.apply_dark_mode_styles()

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
