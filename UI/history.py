from PyQt6 import uic


class HistoryWindow:
    def __init__(self):
        self.history_view = uic.loadUi("UI/history.ui")
        self.history_view.show()
