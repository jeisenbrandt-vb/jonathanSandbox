import sys
from PyQt5.QtWidgets import QApplication, QPushButton

def main():
    print("main");
    #create window
    app = QApplication(sys.argv)

    window = QPushButton("Push Me")
    window.show()

    app.exec()

if __name__ == "__main__":
    main();