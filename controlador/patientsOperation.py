from modelo.Patient import Patient
from modelo.Identifier import Identifier
from modelo.HumanName import HumanName
from modelo.ContactPoint import ContactPoint
from connection import get_connection
from controlador.saveDbOperations import saveIdentifierInDatabase, saveTelecomInDatabase, saveToDatabase

def getAllPatients():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)  # Para devolver resultados como diccionarios

    try:
        # Obtener datos básicos de los pacientes
        query_patients = """
            SELECT ID, IDENTIFIER, FIRST_NAME, LAST_NAME, ACTIVE, GENDER, BIRTH_DATE
            FROM PATIENT;
        """
        cursor.execute(query_patients)
        patients = cursor.fetchall()

        # Para cada paciente, obtener los Identifiers y ContactPoints
        for patient in patients:
            # Obtener Identifiers
            query_identifiers = """
                SELECT TIPO, VALUE
                FROM IDENTIFIER
                WHERE PATIENT_ID = %s;
            """
            cursor.execute(query_identifiers, (patient["ID"],))
            patient["IDENTIFIERS"] = cursor.fetchall()

            # Obtener ContactPoints
            query_contact_points = """
                SELECT SISTEMA, VALUE, USO
                FROM CONTACTPOINT
                WHERE PATIENT_ID = %s;
            """
            cursor.execute(query_contact_points, (patient["ID"],))
            patient["CONTACT_POINTS"] = cursor.fetchall()

        conn.close()
        return patients, "success"

    except Exception as e:
        print(f"Error fetching patients: {e}")
        return [], "error"
    finally:
        cursor.close()
        conn.close()



def getPatientByIdentifier(identifier):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Consulta del paciente
        cursor.execute("SELECT * FROM PATIENT WHERE IDENTIFIER = %s", (identifier,))
        patient = cursor.fetchone()
        
        if not patient:
            return None, "not found"
        
        # Consulta para IDENTIFIERS
        cursor.execute("SELECT * FROM IDENTIFIER WHERE PATIENT_ID = %s", (patient["ID"],))
        patient["IDENTIFIERS"] = cursor.fetchall()

        # Consulta para CONTACT_POINTS
        cursor.execute("SELECT * FROM CONTACTPOINT WHERE PATIENT_ID = %s", (patient["ID"],))
        patient["CONTACT_POINTS"] = cursor.fetchall()

        cursor.close()  # Cerrar el cursor
        conn.close()    # Cerrar la conexión

        return patient, "success"

    except Exception as e:
        print(f"Error fetching patient by identifier: {e}")
        return None, "error"
