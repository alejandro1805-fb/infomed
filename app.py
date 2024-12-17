from flask import Flask, request, jsonify
import jsons
import json
from controlador.patientsOperation import getPatientById, getPatientByIdentifier
from modelo.Identifier import Identifier
from modelo.Patient import Patient
from controlador.saveDbOperations import saveToDatabase
from controlador.patientsOperation import getAllPatients
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Endpoint to retrieve (GET request) Por Documento (identifier)
@app.route('/allpatients', methods=['GET'])
def get_all_patients():
    try:
        logging.info("GET /allpatients - Petición recibida")
        patients_list, status = getAllPatients()
        if status == "success":
            logging.info("GET /allpatients - Respuesta exitosa")
            return jsonify(patients_list), 200
        else:
            logging.error("GET /allpatients - Error al recuperar los datos")
            return jsonify({"error": "Failed to retrieve patients"}), 400
    except Exception as e:
        logging.exception(f"Error en GET /allpatients: {e}")
        return jsonify({"error": str(e)}), 500

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
        else:
            return jsonify({"error": "Failed to save patient"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
