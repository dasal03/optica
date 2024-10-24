import os
import webbrowser
from PyQt6 import uic
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QTableWidgetItem, QStyle, QApplication, QHeaderView)
from DataBase.DataBase import DataBase
from Classes.History import History
from Classes.DocumentType import DocumentType


class MainWindow:
    def __init__(self):
        self.db = DataBase()
        self.history = History(self.db)
        self.main_view = uic.loadUi("UI/main.ui")
        self.init_gui()
        self.load_document_types()
        self.main_view.showMaximized()

    def init_gui(self):
        """Initialize GUI elements and connect signals."""
        self.main_view.btnHistoriaClinica.triggered.connect(self.open_history)
        self.history_view = uic.loadUi("UI/history.ui")
        self.init_table()
        self.history_view.btnSearch.clicked.connect(self.search_history)

    def init_table(self):
        """Initialize the history table and set its headers."""
        self.history_view.tableFiles.setColumnCount(4)
        self.history_view.tableFiles.setHorizontalHeaderLabels(
            [
                "Nombre completo",
                "Fecha de radicación",
                "Fecha de actualización",
                "Acción",
            ]
        )

        header = self.history_view.tableFiles.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        # Set font size for header
        header_font = header.font()
        header_font.setPointSize(12)
        header.setFont(header_font)

    def load_document_types(self):
        """Load document types into the ComboBox."""
        self.history_view.txtDocumentType.clear()
        document_type = DocumentType(self.db)
        document_types = document_type.get_document_types()

        if document_types:
            for doc_type in document_types:
                self.history_view.txtDocumentType.addItem(
                    doc_type["description"], doc_type["document_type_id"]
                )
        else:
            self.history_view.lblError.setText("No se encontraron resultados")

    def open_history(self):
        """Display the history window."""
        self.history_view.lblError.setText("")
        self.history_view.setGeometry(
            QStyle.alignedRect(
                Qt.LayoutDirection.LeftToRight,
                Qt.AlignmentFlag.AlignCenter,
                self.history_view.size(),
                QApplication.primaryScreen().availableGeometry(),
            )
        )
        self.history_view.show()

    def search_history(self):
        """Search history based on user input and populate the table."""
        self.history_view.tableFiles.setRowCount(0)

        data = self.get_search_data()
        if not data:
            return

        response = self.history.search_history(data)
        if response:
            self.populate_table(response)
        else:
            self.history_view.lblError.setText("No se encontraron resultados")

    def get_search_data(self):
        """Extract and validate search input data."""
        document_type_id = self.history_view.txtDocumentType.currentData()
        document_number = self.history_view.txtDocumentNumber.text().strip()

        if document_type_id is None:
            self.history_view.lblError.setText(
                "Seleccione un tipo de documento")
            return None

        if not document_number.isdigit() or len(document_number) < 8:
            self.history_view.lblError.setText(
                "Ingrese un número de documento válido")
            return None

        return {
            "document_type_id": document_type_id,
            "document_number": document_number,
        }

    def populate_table(self, data):
        """Populate the history table with search results."""
        self.history_view.tableFiles.setRowCount(0)

        icon_size = QSize(32, 32)
        self.history_view.tableFiles.setIconSize(icon_size)

        for row_number, row_data in enumerate(data):
            self.history_view.tableFiles.insertRow(row_number)

            # Populate row data
            self.add_table_item(row_number, 0, row_data.get("full_name", ""))
            self.add_table_item(row_number, 1, row_data.get("created_at", ""))
            self.add_table_item(row_number, 2, row_data.get("updated_at", ""))

            # Add download icon
            icon_path = self.get_icon_path("download_icon.png")
            download_icon = QIcon(icon_path)
            download_item = QTableWidgetItem(download_icon, "")

            # Centrar el ícono
            download_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            download_item.setFlags(
                Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

            self.history_view.tableFiles.setItem(row_number, 3, download_item)

            # Attach file URL to the download column
            self.history_view.tableFiles.item(row_number, 3).setData(
                Qt.ItemDataRole.UserRole, row_data.get("file_url", "")
            )

        try:
            self.history_view.tableFiles.cellClicked.disconnect()
        except TypeError:
            pass  # No connection yet

        self.history_view.tableFiles.cellClicked.connect(self.on_file_click)
        self.history_view.tableFiles.setCursor(
            Qt.CursorShape.PointingHandCursor)

    def add_table_item(self, row, column, text):
        """Helper method to add an item to a table cell."""
        item = QTableWidgetItem(str(text))
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.history_view.tableFiles.setItem(row, column, item)

    def get_icon_path(self, icon_name):
        """Construct the absolute path to an icon."""
        return os.path.join(
            os.path.dirname(__file__), f"../assets/{icon_name}")

    def on_file_click(self, row, column):
        """Handle file download when the user clicks the download icon."""
        if column == 3:  # Check if the clicked column is the download column
            file_url = self.history_view.tableFiles.item(row, column).data(
                Qt.ItemDataRole.UserRole
            )
            if file_url:
                self.download_file(file_url)

    def download_file(self, url):
        """Open the file URL in the web browser."""
        try:
            webbrowser.open(url)
        except webbrowser.Error as e:
            self.history_view.lblError.setText(
                f"Error al abrir el archivo: {str(e)}"
            )
