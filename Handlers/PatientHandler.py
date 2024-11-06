from Classes.Patient import Patient
from Utils.EventTools import authorized


@authorized
def patient(event, context, conn):
    patient_class = Patient(conn)

    methods = {
        "GET": patient_class.get_patient_info,
        "POST": patient_class.register_patient,
        "PUT": patient_class.update_patient,
        "DELETE": patient_class.delete_patient,
    }

    method_to_be_executed = methods.get(event["httpMethod"])
    return method_to_be_executed(event)
