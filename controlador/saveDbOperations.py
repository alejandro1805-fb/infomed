from connection import get_connection
import uuid

def saveIdentifierInDatabase(ide, cursor, patId):
    identId = uuid.uuid4()
    query = f"""
        INSERT INTO IDENTIFIER (ID, PATIENT_ID, TIPO, VALUE)
        VALUES
        ('{identId}', '{patId}', '{ide['type']}', '{ide['value']}');
    """
    cursor.execute(query)

def saveTelecomInDatabase(tel, cursor, patId):
    teltId = uuid.uuid4()
    query = f"""
        INSERT INTO CONTACTPOINT (ID, PATIENT_ID, SISTEMA, VALUE, USO)
        VALUES
        ('{teltId}', '{patId}', '{tel['system']}', '{tel['value']}', '{tel['use']}');
    """
    cursor.execute(query)

def saveToDatabase(newPatient):
    conn = get_connection()
    cursor = conn.cursor()
    patId = uuid.uuid4()

    # Insertar en PATIENT
    query = f"""
        INSERT INTO PATIENT (ID, IDENTIFIER, FIRST_NAME, LAST_NAME, ACTIVE, GENDER, BIRTH_DATE)
        VALUES
        ('{patId}', '{newPatient['identifier']}', '{newPatient['name']['given']}', 
         '{newPatient['name']['family']}', {1 if newPatient['active'] else 0}, 
         '{newPatient['gender']}', '{newPatient['birthDate']}');
    """
    cursor.execute(query)
    conn.commit()

    # Insertar en IDENTIFIER
    for ide in newPatient.get("identifiers", []):
        saveIdentifierInDatabase(ide, cursor, patId)
        conn.commit()

    # Insertar en CONTACTPOINT
    for tel in newPatient.get("telecom", []):
        saveTelecomInDatabase(tel, cursor, patId)
        conn.commit()

    cursor.close()
    conn.close()
    return "success"
