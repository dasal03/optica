from PyQt6.QtWidgets import QApplication
from UI.login import Login


class Optica(QApplication):
    def __init__(self):
        super().__init__([])
        self.login = Login()
        self.exec()


if __name__ == "__main__":
    app = Optica()
