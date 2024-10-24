import hashlib
from sqlalchemy.sql.functions import concat
from sqlalchemy import select, insert, update, and_
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Utils.Validations import Validations
from Models.User import UserModel
from Models.DocumentType import DocumentTypeModel


class User:
    """Class for manage user authentication."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations()

    def get_user_data(self, event):
        """Get user data from database."""
        request = get_input_data(event)
        conditions = [UserModel.active == 1]
        user_id = request.get("user_id", 0)

        if user_id:
            conditions.append(UserModel.user_id == user_id)

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
                UserModel.document_number,
                UserModel.birthdate,
                UserModel.created_at,
                UserModel.updated_at,
            ).join(
                DocumentTypeModel,
                and_(
                    UserModel.document_type_id ==
                    DocumentTypeModel.document_type_id,
                    DocumentTypeModel.active == 1
                ), isouter=True
            ).where(*conditions)
        )

        response = self.db.query(stmt).as_dict()

        if response:
            status_code = 200
            data = response
        else:
            status_code = 404
            data = []

        return {"statusCode": status_code, "data": data}

    def register_user(self, event):
        """Get form data and create new user"""
        request = get_input_data(event)

        # Extract and validate data
        validation_errors = self.validations.validate(
            self.validations.param("first_name", request["first_name"], str),
            self.validations.param("last_name", request["last_name"], str),
            self.validations.param("username", request["username"], str),
            self.validations.param("password", request["password"], str),
            self.validations.param("email", request["email"], str),
            self.validations.param(
                "document_type_id", request["document_type_id"], int
            ),
            self.validations.param(
                "document_number", request["document_number"], int),
        )

        if validation_errors:
            raise CustomException(validation_errors)

        self._create_user(request)

    def _create_user(self, request):
        hashed_password = hashlib.sha256(
            request["password"].encode()).hexdigest()
        stmt = insert(UserModel).values(
            first_name=request["first_name"],
            last_name=request["last_name"],
            username=request["username"],
            password=hashed_password,
            email=request["email"],
            document_type_id=request["document_type_id"],
            document_number=request["document_number"],
        )
        if request["profile_picture"]:
            stmt.values(profile_picture=request["profile_picture"])

        user_id = self.db.add(stmt)
        return user_id if user_id else None

    def update_user(self, event):
        """Receives user data and updates it in the database."""
        request = get_input_data(event)
        user_id = request.get("user_id", 0)

        self.validations.records(
            conn=self.db,
            model=UserModel,
            pk=user_id,
            error_class=CustomException("User not found"),
        )

        stmt = (
            update(UserModel)
            .where(UserModel.user_id == user_id, UserModel.active == 1)
            .values(**request)
        )

        is_updated = self.db.update(stmt)
        return is_updated

    def delete_user(self, user_id):
        pass
