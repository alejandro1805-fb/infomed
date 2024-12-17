from flask import Flask, request, jsonify
import jsons
import json
from controlador.patientsOperation import getPatientByIdentifier
from modelo.Identifier import Identifier
from modelo.Patient import Patient
from controlador.saveDbOperations import saveToDatabase
from controlador.patientsOperation import getAllPatients, getPatientByIdentifier
import logging

app = Flask(__name__)

# Endpoint to retrieve (GET request) Por Documento (identifier)
@app.route('/allpatients', methods=['GET'])
def get_all_patients():
    try:
        logging.info("GET /allpatients - Petición recibida")
        patients_list, status = getAllPatients()
        if status == "success":
            return jsonify(patients_list), 200
        else:
            return jsonify({"error": "Failed to retrieve patients"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/patients/<int:identifier>', methods=['GET'])
def get_patient_by_identifier(identifier):
    try:
        # Llamada a la función que obtiene un paciente específico
        patient_data, status = getPatientByIdentifier(identifier)
        if status == "success":
            return jsonify(patient_data), 200  # Devuelve el paciente en formato JSON
        else:
            return jsonify({"error": "Patient not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

        # Verificar si ya existe un paciente activo con el mismo IDENTIFIER
        existing_patient = find_patient_by_identifier(new_patient["identifier"])

        if existing_patient and existing_patient["active"]:  # Paciente activo ya existe
            return jsonify({"error": f"Patient with IDENTIFIER {new_patient['identifier']} already exists and is active"}), 400

        # Guardar en base de datos
        status = saveToDatabase(new_patient)

        if status == "success":
            return jsonify({"message": "Patient was saved successfully"}), 201
        else:
            return jsonify({"error": "Failed to save patient"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)