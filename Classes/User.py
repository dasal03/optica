import hashlib
from sqlalchemy.sql.functions import concat
from sqlalchemy import select, insert, update, and_
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Utils.Validations import Validations
from Models.User import UserModel
from Models.DocumentType import DocumentTypeModel


class User:
    """Class for manage users."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations(self.db)

    def get_user_data(self, event):
        """Get user data from database."""
        request = get_input_data(event)
        conditions = {"active": 1}

        # Dinamic conditions
        if request:
            for key, value in request.items():
                conditions[key] = value

        # TODO: Add relation with roles model
        stmt = (
            select(
                UserModel.user_id,
                concat(
                    UserModel.first_name, " ", UserModel.last_name
                ).label("full_name"),
                UserModel.username,
                UserModel.email,
                UserModel.profile_picture,
                DocumentTypeModel.description.label("document_type"),
                UserModel.document_type_id,
                UserModel.document_number,
                UserModel.date_of_birth,
                UserModel.created_at,
                UserModel.updated_at,
            )
            .filter_by(**conditions)
            .join(
                DocumentTypeModel,
                and_(
                    UserModel.document_type_id ==
                    DocumentTypeModel.document_type_id,
                    DocumentTypeModel.active == 1
                ), isouter=True
            )
        )
        response = self.db.query(stmt).as_dict()

        status_code = 200 if response else 404
        data = response if response else []

        return {"statusCode": status_code, "data": data}

    def register_user(self, event):
        """Get form data and create new user"""
        request = get_input_data(event)
        first_name = request.get("first_name", "")
        last_name = request.get("last_name", "")
        username = request.get("username", "")
        password = request.get("password", "")
        email = request.get("email", "")
        document_type_id = request.get("document_type_id", 0)
        document_number = request.get("document_number", 0)
        date_of_birth = request.get("date_of_birth", "")
        role_id = request.get("role_id", 0)
        profile_picture = request.get("profile_picture", "")

        validation_list = [
            self.validations.param("first_name", str, first_name),
            self.validations.param("last_name", str, last_name),
            self.validations.param("username", str, username),
            self.validations.param("password", str, password),
            self.validations.param("email", str, email),
            self.validations.param("document_type_id", int, document_type_id),
            self.validations.param("document_number", int, document_number),
            self.validations.param("date_of_birth", str, date_of_birth),
            self.validations.param("role_id", int, role_id),
        ]

        if profile_picture:
            validation_list.append(
                self.validations.param("profile_picture", str, profile_picture)
            )

        validated = self.validations.validate(validation_list, cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        self.validate_username_exist(username)

        # Encrypt received password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        stmt = insert(UserModel).values(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_password,
            email=email,
            document_type_id=document_type_id,
            document_number=document_number,
            date_of_birth=date_of_birth,
            role_id=role_id,
            profile_picture=profile_picture
        )
        user_id = self.db.add(stmt)

        if user_id:
            status_code = 201
            data = {"user_id": user_id}
        else:
            status_code = 400
            data = {}

        return {"statusCode": status_code, "data": data}

    def validate_username_exist(self, username: str) -> None:
        """
        Validate that the username exists.
        Args:
            username (str): The user name for cognito.
        Raises:
            ValueError: If the username exist or is invalid.
        """
        user = self.db.query(
            select(UserModel.username).filter_by(username=username, active=1)
        ).first()

        if user:
            raise CustomException(
                "A User with the specified username already exists"
            )

    def update_user(self, event):
        """Receives user data and updates it in the database."""
        request = get_input_data(event)
        user_id = request.get("user_id", 0)
        username = request.get("username", "")
        password = request.get("password", "")

        self.validations.records(
            conn=self.db,
            model=UserModel,
            pk=user_id,
            error_class=CustomException("The provided user does not exist"),
            as_dict=True
        )

        self.validate_username_exist(username)
        request["password"] = hashlib.sha256(password.encode()).hexdigest()

        affected_rows = self.db.update(
            update(UserModel)
            .where(UserModel.user_id == user_id)
            .values(**request)
        )

        if affected_rows:
            status_code = 200
            data = "User updated successfully"
        else:
            status_code = 400
            data = "The user couldn't be updated. No properties changed"

        return {"statusCode": status_code, "data": data}

    def delete_user(self, event):
        user_id = event.get("user_id", 0)

        self.validations.records(
            conn=self.db,
            model=UserModel,
            pk=user_id,
            error_class=CustomException("The provided user does not exist"),
            as_dict=True
        )

        stmt = (
            update(UserModel)
            .where(UserModel.user_id == user_id)
            .values(active=0)
        )
        affected_rows = self.db.update(stmt)

        if affected_rows:
            status_code = 200
            data = "User deleted successfully"
        else:
            status_code = 400
            data = "The user couldn't be deleted. No properties changed"

        return {"statusCode": status_code, "data": data}
