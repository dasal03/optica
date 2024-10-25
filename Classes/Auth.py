import hashlib
from sqlalchemy import select
from Utils.GeneralTools import get_input_data
from Utils.ExceptionsTools import CustomException
from Utils.Validations import Validations
from Models.User import UserModel


class Auth:
    """Class for manage user authentication."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations(self.db)

    def login(self, event):
        """Validate user credentials and return user id if user exists."""
        request = get_input_data(event)
        username = request.get("username", "")
        password = request.get("password", "")

        validation_errors = [
            self.validations.param("username", str, username),
            self.validations.param("password", str, password)
        ]

        validated = self.validations.validate(validation_errors, cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        # SELECT: search if user exists
        response = self.db.query(
            select(UserModel).where(UserModel.username == username)
        ).first().as_dict()

        status_code = 400
        data = "Invalid username or password"

        if response:
            # Encrypt received password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Compare received password with hashed password
            if hashed_password == response["password"]:
                status_code = 200
                # Change with user token
                data = {"user_id": response["user_id"]}

        return {"statusCode": status_code, "data": data}
