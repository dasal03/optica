import os
from sqlalchemy import select, and_
from sqlalchemy.sql.functions import concat
from Utils.Validations import Validations
from Models.User import UserModel
from Models.History import HistoryModel
from Models.DocumentType import DocumentTypeModel


class History:
    """Class for manage clinical history."""
    def __init__(self, db):
        self.db = db
        self.validations = Validations()

    def search_history(self, data):
        """Get all clinical history for a specific document."""

        validation_errors = self.validations.validate(
            self.validations.param(
                "document_number", data["document_number"], int),
            self.validations.param(
                "document_type_id", data["document_type_id"], int)
        )

        if validation_errors:
            raise AssertionError(validation_errors)

        stmt = (
            select(
                UserModel.user_id,
                concat(
                    UserModel.first_name, " ", UserModel.last_name
                ).label("full_name"),
                HistoryModel.file_url,
                HistoryModel.created_at,
                HistoryModel.updated_at,
            )
            .join(HistoryModel, HistoryModel.user_id == UserModel.user_id)
            .join(
                DocumentTypeModel,
                UserModel.document_type_id ==
                DocumentTypeModel.document_type_id
            )
            .filter(
                UserModel.document_number == data["document_number"],
                and_(
                    UserModel.document_type_id == data["document_type_id"],
                    DocumentTypeModel.active == 1
                )
            )
        )
        results = self.db.query(stmt).as_dict()
        base_dir = os.path.abspath("temp")

        for result in results:
            # Build absolute path
            file_name = result["file_url"]
            result["file_url"] = os.path.join(base_dir, f"{file_name}.pdf")

        return results if results else []
