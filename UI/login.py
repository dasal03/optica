from PyQt6 import uic
from DataBase.DataBase import DataBase
from UI.main import MainWindow
from UI.register import Register
from Classes.Auth import Auth


class Login:
    ERROR_MSGS = {
        "username": "Por favor, ingrese un nombre de usuario válido",
        "password": "Por favor, ingrese una contraseña válida"
    }

    def __init__(self):
        self.db = DataBase()
        self.auth = Auth(self.db)
        self.login_view = uic.loadUi("UI/login.ui")
        self.login_view.lblError.setText("")
        self.init_gui()
        self.login_view.show()

    def login(self):
        """Validate user credentials and login if valid"""
        data = self.get_login_data()
        validation_error = self.validate_data(data)

        if validation_error:
            self.login_view.lblError.setText(validation_error)
            return

        response = self.auth.login(data)

        if response:
            self.main = MainWindow()
            self.login_view.hide()
        else:
            self.login_view.lblError.setText("Credenciales inválidas")

    def get_login_data(self):
        """Get form data"""
        return {
            "username": self.login_view.txtUsername.text().strip(),
            "password": self.login_view.txtPassword.text().strip(),
        }

    def validate_data(self, data):
        """Validates registration data, returns an error message or None."""
        for field, error_msg in self.ERROR_MSGS.items():
            if not data.get(field):
                return error_msg
        return None

    def open_register(self):
        """Open register view"""
        self.login_view.hide()
        self.register = Register()
        self.register.register_view.show()

    def init_gui(self):
        """Calls methods to initialize GUI components"""
        self.login_view.btnLogin.clicked.connect(self.login)
        self.login_view.btnRegister.clicked.connect(self.open_register)
