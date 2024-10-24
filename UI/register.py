from PyQt6 import uic
from UI.main import MainWindow
from DataBase.DataBase import DataBase
from Classes.DocumentType import DocumentType
from Classes.Auth import Auth


class Register:
    def __init__(self):
        self.db = DataBase()
        self.auth = Auth(self.db)
        self.register_view = uic.loadUi("UI/register.ui")
        self.register_view.lblError.setText("")
        self.init_gui()
        self.load_document_types()

    def load_document_types(self):
        """Load document types into the ComboBox."""
        self.register_view.txtDocumentType.clear()
        document_type = DocumentType(self.db)
        document_types = document_type.get_document_types()

        if document_types:
            for doc_type in document_types:
                self.register_view.txtDocumentType.addItem(
                    doc_type["description"], doc_type["document_type_id"]
                )
        else:
            self.register_view.lblError.setText("No se encontraron resultados")

    def register(self):
        """Get register form data and create new user"""
        data = self.get_register_data()
        response = self.auth.register_user(data)
        # self.register_view.lblError.setText(validation_error)

        if response:
            self.main = MainWindow()
            self.register_view.hide()
        else:
            self.register_view.lblError.setText("Error al registrar usuario")

    def get_register_data(self):
        """Returns a dictionary with the data from the registration form."""
        return {
            "first_name": self.register_view.txtFirstName.text().strip(),
            "last_name": self.register_view.txtLastName.text().strip(),
            "username": self.register_view.txtUsername.text().strip(),
            "password": self.register_view.txtPassword.text().strip(),
            "email": self.register_view.txtEmail.text().strip(),
            "document_type_id": (
                self.register_view.txtDocumentType.currentData()),
            "document_number": (
                self.register_view.txtDocumentNumber.text().strip()),
            "birthdate": self.register_view.txtBirthdate.currentData()
        }

    def init_gui(self):
        """Initializes the GUI components and connects signals."""
        self.register_view.btnRegister.clicked.connect(self.register)
