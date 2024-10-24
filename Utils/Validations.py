from sqlalchemy import select
from Utils.GeneralTools import as_list
from Utils.QueryTools import get_pk_name


class Validations:
    """Class for data validation."""

    @classmethod
    def records(
        cls,
        conn,
        model,
        pk,
        pk_name: str = None,
        column_active_name="active",
        column_active_value=1,
        error_class=KeyError,
        as_dict=False,
        **aditional_filter
    ) -> list:
        """
        Validate if a record exists in the database.
        """
        pk_list = as_list(pk)
        records = []
        for pk in pk_list:
            # Querying by primary key
            record = conn.query(
                select(model).filter_by(
                    **{
                        pk_name or get_pk_name(model): pk,
                        column_active_name: column_active_value,
                    },
                    **aditional_filter,
                )
            ).first()
            if not record:  # If not found raise error
                raise error_class
            records.append(record.as_dict() if as_dict else record)
        return records

    @staticmethod
    def param(field_name, value, expected_type, min_len=None, max_len=None):
        """
        Validate an individual parameter for type,
            minimum length, and maximum length.

        :param field_name: The name of the field.
        :param value: The value to validate.
        :param expected_type: The expected type for the field.
        :param min_len: Minimum length for the field (if it's a string).
        :param max_len: Maximum length for the field (if it's a string).
        :return: A dictionary with errors, if any.
        """
        errors = []

        # Check type
        if not isinstance(value, expected_type):
            errors.append(
                f"Field '{field_name}' must be of type "
                f"{expected_type.__name__}."
            )

        # Check minimum length (only for strings)
        if (
            isinstance(value, str) and
            min_len is not None and len(value) < min_len
        ):
            errors.append(
                f"Field '{field_name}' must be at least "
                f"{min_len} characters long."
            )

        # Check maximum length (only for strings)
        if (
            isinstance(value, str) and max_len is not None
            and len(value) > max_len
        ):
            errors.append(
                f"Field '{field_name}' exceeds maximum length of "
                f"{max_len} characters."
            )

        return {field_name: errors} if errors else None

    @staticmethod
    def validate(*param_results):
        """
        Validate multiple parameters and accumulate errors.

        :param param_results: A variable number of validation results
            (from param method).
        :return: A list of accumulated errors, or None if no errors.
        """
        errors = []

        for result in param_results:
            if result:
                for field, field_errors in result.items():
                    if field_errors:
                        errors.append({field: field_errors})

        return errors if errors else None
