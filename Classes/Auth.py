import hashlib
from sqlalchemy import select
from Utils.Validations import Validations
from Models.User import UserModel


class Auth:
    """Class for manage user authentication."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations()

    def login(self, data):
        """Validate user credentials and return user id if user exists."""

        validation_errors = self.validations.validate(
            self.validations.param("username", data["username"], str),
            self.validations.param("password", data["password"], str)
        )

        if validation_errors:
            raise AssertionError(validation_errors)

        # SELECT: search if user exists
        response = (
            self.db.query(
                select(UserModel.user_id, UserModel.password).where(
                    UserModel.username == data["username"]
                )
            )
            .first()
            .as_dict()
        )

        if response:
            # Encrypt received password
            hashed_password = hashlib.sha256(
                data["password"].encode()
            ).hexdigest()
            # Compare received password with hashed password
            if hashed_password == response["password"]:
                return response["user_id"]
        else:
            return None
