from connection import get_connection
import uuid

def saveIdentifierInDatabase(ide,cursor,patId):
    identId = uuid.uuid4()
    query = f"""
        INSERT INTO IDENTIFIER (ID, PATIENT_ID, TYPE, VALUE)
        VALUES
        ('{identId}','{patId}','{ide.type}','{ide.value}');
    """
    cursor.execute(query)

def saveTelecomInDatabase(tel,cursor,patId):
    teltId = uuid.uuid4()
    query = f"""
        INSERT INTO CONTACT_POINT (ID, PATIENT_ID, USO, SISTEMA, VALUE)
        VALUES
        ('{teltId}','{patId}','{tel.system}','{tel.value}','{tel.use}');
    """
    cursor.execute(query)

def saveToDatabase(newPatient):
    conn = get_connection()
    cursor = conn.cursor()
    # Create pat_id
    patId = uuid.uuid4()
    #
    query = f"""
        INSERT INTO PATIENT (ID, NAME, GENDER, BIRTH_DATE)
        VALUES
        ('{patId}','{newPatient.name.family}','{newPatient.gender}','{newPatient.birthDate}');
    """
    cursor.execute(query)
    conn.commit()
    #
    # identifiers
    for ide in newPatient.identifier:
        saveIdentifierInDatabase(ide,cursor,patId)
        conn.commit()
    #
    # telecoms
    for tel in newPatient.telecom:
        saveTelecomInDatabase(tel,cursor,patId)
        conn.commit()
    #
    cursor.close()
    conn.close()
    return "success"
