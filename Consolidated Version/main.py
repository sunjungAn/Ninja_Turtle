import sys
from PyQt5.QtWidgets import QApplication, QDialog
from ui import Ui_Ninja_Turtle

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Ninja_Turtle = QDialog()
    ui = Ui_Ninja_Turtle()
    ui.setupUi(Ninja_Turtle)
    Ninja_Turtle.show()
    sys.exit(app.exec_())
