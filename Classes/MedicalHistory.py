from sqlalchemy import select, and_, insert
from sqlalchemy.sql.functions import concat
from Utils.ExceptionsTools import CustomException
from Utils.GeneralTools import get_input_data
from Utils.PdfGenerator import PDFGenerator
from Utils.Validations import Validations
from Classes.Patient import Patient
from Models.Consultation import ConsultationModel
from Models.MedicalHistory import MedicalHistoryModel
from Models.MedicalHistoryTrazability import MedicalHistoryTrazabilityModel
from Models.Patient import PatientModel
from Models.Template import TemplateModel

# Constants
MEDICAL_HISTORY = 1


class MedicalHistory:
    """API to manage and retrieve medical history details."""

    def __init__(self, db):
        self.db = db
        self.validations = Validations(db)
        self.pdf_generator = PDFGenerator()

    def get_template(self, operation_id):
        """Retrieve template data from the database."""
        result = self.db.query(
            select(TemplateModel.content).where(
                TemplateModel.operation_id == operation_id
            )
        ).first()

        if not result:
            raise CustomException("Template data not found.")
        return result.content

    def get_medical_history(self, event):
        """Retrieve and list medical history details for a patient."""
        request = get_input_data(event)
        document_number = request.get("document_number")

        validation_result = self.validations.validate([
            self.validations.param("document_number", int, document_number)
        ])

        if not validation_result["isValid"]:
            raise CustomException(validation_result["data"])

        # Retrieve patient information
        patient_class = Patient(self.db)
        patient_data = patient_class.get_patient_info(
            {
                "httpMethod": "GET",
                "pathParameters": {"document_number": document_number},
            }
        )

        if patient_data["statusCode"] != 200:
            raise CustomException("Patient data not found.")

        patient_id = patient_data["data"][0]["patient_id"]

        # Get medical history data
        medical_history_data = self._fetch_medical_history(patient_id)

        if not medical_history_data:
            raise CustomException("No medical history found for this patient.")

        return {
            "statusCode": 200,
            "data": medical_history_data
        }

    def generate_medical_history_pdf(self, event):
        """Generate a PDF for the patient's medical history."""
        try:
            patient_data = get_input_data(event)
            medical_history_id = patient_data.get("medical_history_id", 0)

            output_file_path = (
                f"{patient_data['document_number']}_medical_history.pdf"
            )

            # Ensure the template data is loaded
            template = self.get_template(MEDICAL_HISTORY)

            self.pdf_generator.generate_pdf(
                template=template,
                output_pdf_name=output_file_path,
                content=patient_data
            )

            self._record_trazability(medical_history_id, output_file_path)

            return {"statusCode": 200, "data": output_file_path}
        except Exception as e:
            raise CustomException(f"Error generating PDF: {str(e)}")

    def _fetch_medical_history(self, patient_id):
        """Retrieve detailed medical history for the given patient."""
        stmt = (
            select(
                PatientModel.patient_id,
                concat(
                    PatientModel.first_name, " ", PatientModel.last_name
                ).label("patient_name"),
                PatientModel.email,
                PatientModel.document_type_id,
                PatientModel.document_number,
                PatientModel.date_of_birth,
                PatientModel.phone_number.label("contact_number"),
                PatientModel.address.label("patient_address"),
                ConsultationModel.created_at.label("consultation_date"),
                ConsultationModel.reason.label("visit_reason"),
                MedicalHistoryModel.medical_history_id,
                MedicalHistoryModel.visual_acuity_re,
                MedicalHistoryModel.visual_acuity_le,
                MedicalHistoryModel.near_vision_re,
                MedicalHistoryModel.near_vision_le,
                MedicalHistoryModel.distance_vision_re,
                MedicalHistoryModel.distance_vision_le,
                MedicalHistoryModel.past_medical_conditions,
                MedicalHistoryModel.current_medication,
                PatientModel.known_allergies,
                MedicalHistoryModel.fundus_exam,
                MedicalHistoryModel.intraocular_pressure_re,
                MedicalHistoryModel.intraocular_pressure_le,
                MedicalHistoryModel.diagnosis,
                MedicalHistoryModel.treatment_plan,
                MedicalHistoryModel.additional_notes
            )
            .join(
                MedicalHistoryModel,
                MedicalHistoryModel.patient_id == PatientModel.patient_id
            )
            .join(
                ConsultationModel,
                and_(
                    PatientModel.patient_id == ConsultationModel.patient_id
                ), isouter=True
            )
            .where(
                and_(
                    PatientModel.patient_id == patient_id,
                    PatientModel.active == 1
                )
            )
        )
        result = self.db.query(stmt).first().as_dict()
        return result[0] if result else None

    def _record_trazability(self, medical_history_id, file_url):
        """Record changes or access in the medical history trazability."""
        insert_stmt = insert(MedicalHistoryTrazabilityModel).values(
            medical_history_id=medical_history_id, file_url=file_url
        )
        self.db.add(insert_stmt)
