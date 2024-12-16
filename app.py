from flask import Flask, request, jsonify
import jsons
import json
from controlador.patientsOperation import getPatientById, getPatientByIdentifier
from modelo.Identifier import Identifier
from modelo.Patient import Patient
from controlador.saveDbOperations import saveToDatabase

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
    try:
        newPatientDict = request.get_json()

        # Construir el diccionario del paciente
        new_patient = {
            "identifier": newPatientDict.get("IDENTIFIER"),
            "name": {
                "given": newPatientDict["FIRST_NAME"],
                "family": newPatientDict["LAST_NAME"]
            },
            "active": newPatientDict.get("ACTIVE", 1),  # Por defecto activo
            "gender": newPatientDict["GENDER"],
            "birthDate": newPatientDict["BIRTH_DATE"],
            "identifiers": newPatientDict.get("IDENTIFIERS", []),
            "telecom": newPatientDict.get("CONTACT_POINTS", [])
        }

        # Guardar en base de datos
        status = saveToDatabase(new_patient)

        if status == "success":
            return jsonify({"message": "Patient was saved successfully"}), 201
        elif status == "error: duplicate_identifier":
            return jsonify({"error": "A patient with this IDENTIFIER already exists"}), 409  # 409 Conflict
        else:
            return jsonify({"error": "Failed to save patient"}), 400


    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
