import os
import jwt
import hashlib
from datetime import datetime, timedelta
from sqlalchemy import select
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Models.User import UserModel
from Utils.Validations import Validations

SECRET_KEY = os.getenv("SECRET_KEY")


class Auth:
    """Class for manage user authentication."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations(self.db)

    def login(self, event):
        """Validate user credentials and return token if user exists."""
        request = get_input_data(event)
        username = request.get("username", "")
        password = request.get("password", "")

        validated = self.validations.validate([
            self.validations.param("username", str, username),
            self.validations.param("password", str, password),
        ], cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        # SELECT: search if user exists
        response = self.db.query(
            select(UserModel.user_id, UserModel.password)
            .where(UserModel.username == username)
        ).first()

        status_code = 400
        data = "Invalid username or password"

        if response:
            # Encrypt received password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # Compare received password with hashed password
            if hashed_password == response.password:
                status_code = 200
                user_id = response.user_id

                exp = datetime.utcnow() + timedelta(hours=1)

                token = jwt.encode({
                    "user_id": user_id,
                    "exp": exp,
                }, SECRET_KEY, algorithm="HS256")

                data = {"token": token}

        return {"statusCode": status_code, "data": data}
