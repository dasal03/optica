import os
from sqlalchemy import select, and_
from sqlalchemy.sql.functions import concat
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Utils.Validations import Validations
from Models.User import UserModel
from Models.History import HistoryModel
from Models.DocumentType import DocumentTypeModel


class History:
    """Class for manage clinical history."""
    def __init__(self, db):
        self.db = db
        self.validations = Validations(self.db)

    def search_history(self, event):
        """Get all clinical history for a specific document."""
        request = get_input_data(event)
        document_type_id = request.get("document_type_id", 0)
        document_number = request.get("document_number", 0)
        base_dir = os.path.abspath("temp")

        validation_list = [
            self.validations.param("document_type_id", int, document_type_id),
            self.validations.param("document_number", int, document_number)
        ]

        validated = self.validations.validate(validation_list, cast=True)

        if not validated["isValid"]:
            raise CustomException(validated["data"])

        stmt = (
            select(
                UserModel.user_id,
                concat(UserModel.first_name, " ", UserModel.last_name).label(
                    "full_name"
                ),
                HistoryModel.file_url,
                HistoryModel.created_at,
                HistoryModel.updated_at,
            )
            .join(HistoryModel, HistoryModel.user_id == UserModel.user_id)
            .join(
                DocumentTypeModel,
                and_(
                    UserModel.document_type_id ==
                    DocumentTypeModel.document_type_id,
                    DocumentTypeModel.active == 1
                ),
            )
            .where(
                UserModel.document_number == document_number,
                UserModel.document_type_id == document_type_id
            )
        )
        results = self.db.query(stmt).as_dict()

        if results:
            for result in results:
                # Build absolute path
                file_name = result["file_url"]
                result["file_url"] = os.path.join(base_dir, f"{file_name}.pdf")

            status_code = 200
            data = results
        else:
            status_code = 404
            data = []

        return {"statusCode": status_code, "data": data}

    def create_history(self, data):
        pass

    def update_history(self, data):
        pass

    def delete_history(self, data):
        pass
