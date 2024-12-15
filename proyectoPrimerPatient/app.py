from flask import Flask, request
import jsons
import json
from controlador.patientsOperation import getPatientById, getPatientByIdentifier
from modelo.Identifier import Identifier
from modelo.Patient import Patient

app = Flask(__name__)


# Endpoint to retrieve (GET request) Por Documento (identifier)
@app.route('/patient', methods=['GET'])
def get_patients():
    type = request.args.get('type')
    value = request.args.get('value')
    # Consistencia
    if type is None or value is None:
        return '''<h1>Not valid type or value</h1>''',400
    # Siguientes pasos
    ident = Identifier(type,value)
    myPatient,status = getPatientByIdentifier(ident)
    if status == "success":
        return jsons.dump(myPatient),200
    elif "noExiste":
        return status,201
    else:
        return status,400


@app.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient_by_id(patient_id):
    # Assuming getPatientById is a function that retrieves a patient by their ID
    myPatient, status = getPatientById(patient_id)  
    
    if status == "success":
        return jsons.dump(myPatient), 200  # Use 200 OK for successful retrieval
    else:
        return {'error': f'Patient with ID {patient_id} not found'}, 404  # Return 404 if not found



# Endpoint to add a new book (POST request)
@app.route('/patients', methods=['POST'])
def add_patient():
    newPatientDict = json.loads(request.data)
    newPatient = Patient(
        newPatientDict["name"],
        [Identifier(f["type"],f["value"]) for f in newPatientDict["identifiers"]],
        newPatientDict["gender"],
        newPatientDict["dob"],
        True
    )
    status = newPatient.save_to_database()
    if status == "success":
        return "Patient was saved",201
    return status

if __name__ == '__main__':
    app.run(debug=True)
