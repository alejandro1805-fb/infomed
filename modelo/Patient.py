import dateparser
from modelo.Identifier import Identifier
from modelo.ContactPoint import ContactPoint
from controlador.saveDbOperations import saveToDatabase  # Importar la función saveToDatabase

class Patient:
    
    def __init__(self, inputDict):
        # Datos básicos del paciente
        self.active = inputDict.get("active", 1)  # Por defecto activo
        self.identifier = inputDict.get("IDENTIFIER", "")  # Identificador principal
        self.gender = inputDict["gender"]
        self.birthDate = dateparser.parse(inputDict["birthDate"])
        
        # Nombre del paciente
        self.first_name = inputDict["name"]["given"]
        self.last_name = inputDict["name"]["family"]
        
        # Identificadores secundarios
        self.identifiers = [
            Identifier(type=ident["type"], value=ident["value"]) 
            for ident in inputDict.get("identifiers", [])
        ]
        
        # Contactos del paciente (teléfonos, etc.)
        self.telecom = [
            ContactPoint(system=tel["system"], value=tel["value"], use=tel["use"])
            for tel in inputDict.get("telecom", [])
        ]

    def save_to_database(self):
        """Guarda el paciente en la base de datos usando saveToDatabase."""
        # Guardar el paciente y devolver el resultado
        return saveToDatabase({
            "identifier": self.identifier,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "active": self.active,
            "gender": self.gender,
            "birthDate": self.birthDate,
            "identifiers": [vars(ident) for ident in self.identifiers],
            "telecom": [vars(contact) for contact in self.telecom]
        })

    def cambiarGenero(self):
        """Cambia el género del paciente."""
        if self.gender == 'F':
            self.gender = 'M'
        elif self.gender == 'M':
            self.gender = 'F'


if __name__ == "__main__":
    import json
    aleJson = """
    {
        "IDENTIFIER": "12345678",
        "active": true,
        "name": {
            "family": "Perez",
            "given": "Juan"
        },
        "identifiers": [
            {"type": "CC", "value": "12345678"}
        ],
        "telecom": [
            {"system": "phone", "value": "3131234567", "use": "mobile"},
            {"system": "phone", "value": "6019413574", "use": "home"}
        ],
        "gender": "M",
        "birthDate": "1990-01-01"
    }
    """
    aleDict = json.loads(aleJson)
    aleP = Patient(aleDict)
    result = aleP.save_to_database()
    print(f"Resultado de guardar en base de datos: {result}")
