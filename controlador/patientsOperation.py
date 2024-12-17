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
                SELECT SISTEMA, VALUE, USO AS use
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


def getPatientById(p_id):
    conn = get_connection()
    query = f"""
        SELECT p.PATIENT_ID, p.NAME, p.GENDER, p.BIRTHDATE  , i.TYPE, i.VALUE
        FROM PATIENT p
        INNER JOIN IDENTIFIER i
        ON p.ID=i.PATIENT_ID
        WHERE p.ID='{p_id}';
    """
    cursor = conn.cursor()
    cursor.execute(query)
    results=cursor.fetchall()
    if len(results)==0:
        conn.close()
        return None,"No registered patient"
    identifiersList = list()
    for row in results:
        p_id = row[0]
        name = row[1]
        gender = row[2]
        dob = row[3]
        identifiersList.append(Identifier(row[4]),row[5])
    conn.close()
    return Patient(name,identifiersList,gender,dob,p_id),"success"


def getPatientByIdentifier(ident:Identifier):
    conn = get_connection()
    cursor = conn.cursor()
    ## Verificar existencia en BD
    try:
        query = f"""
            SELECT PATIENT_ID
            FROM IDENTIFIER
            WHERE TYPE='{ident.type}' AND VALUE='{ident.value}';
        """
        cursor.execute(query)
        resultPatId=cursor.fetchone()
        #
        if resultPatId is None or len(resultPatId)==0:
            cursor.close()
            conn.close()
            return None,"noExiste"
    except:
        cursor.close()
        conn.close()
        return None, 'fallaInterna'

    #
    ## Consultar Patients
    query = f"""
        SELECT FIRST_NAME, LAST_NAME, ACTIVE, GENDER, BIRTH_DATE
        FROM PATIENT
        WHERE PATIENT_ID='{resultPatId[0]}';
    """
    cursor.execute(query)
    resultPatientsList=cursor.fetchone()
    #
    ## Consultar Identifiers
    query = f"""
        SELECT TYPE, VALUE
        FROM IDENTIFIER
        WHERE PATIENT_ID='{resultPatId[0]}';
    """
    cursor.execute(query)
    resultIdentifiers=cursor.fetchall()
    #
    listIdent = list()
    for idList in resultIdentifiers:
        listIdent.append(
            {
                "type":idList[0],
                "value":idList[1]
            }
        )
    cursor.close()
    conn.close()
    #
    ## Consultar Contact Point
    query= f"""
        SELECT SISTEMA, VALUE, USO
        FROM CONTACTPOINT
        WHERE PATIENT_ID='{resultPatId[0]}';
    """
    cursor.execute(query)
    resultsContactPointList=cursor.fetchall()
    
    listContactPoint = list()
    for tels in resultsContactPointList:
        listContactPoint.append(
            {
                'system':tels[0],
                'value':tels[1],
                'use':tels[2]
            }
        )
    cursor.close()
    conn.close()

    # Consultar Patient
    #
    patDict = dict()
    patDict["Identifier"] = listIdent
    patDict["contactPoint"] = listContactPoint
    patDict["name"] = {
        "family":resultPatientsList[0],
        "given":resultPatientsList[1],
        "prefix":resultPatientsList[2]
    }
    patDict["active"] = True
    patDict["gender"] = resultPatientsList[4]
    patDict["birthdate"] = resultPatientsList[3].strftime['%Y-%m-%d']
    #
    myPatient  = Patient(
        patDict
    )
    cursor.close()
    conn.close()
    return myPatient,"success"

