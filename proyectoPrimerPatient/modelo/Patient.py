import dateparser
from Identifier import Identifier
from ContactPoint import ContactPoint
from HumanName import HumanName

class Patient:
    
    def __init__(self,inputDict):
        self.active = inputDict["active"]
        self.identifier = []
        for ident in inputDict["identifier"]:
            self.identifier.append(
                Identifier(type=ident['type'],value=ident['value'])
            )
        self.gender = inputDict["gender"]
        self.birthDate = dateparser.parse(inputDict["birthDate"])
        self.name= HumanName(family=inputDict['name']['family'],given=inputDict['name']['given'],prefix=inputDict['name']['prefix'])
        self.telecom=[ContactPoint(system=tel['system'], value=tel['value'], use=tel['use']) for tel in inputDict['telecom']]

    def cambiarGenero(self):
        if self.gender=='F':
            self.gender='M'
        elif self.gender=='M':
            self.gender='F'
    
    def save_to_database(self):
        pass
        
if __name__ == "__main__":
    import json
    aleJson = """
    {
        "identifier":[
            {
                "type":"CC",
                "value":"1011089600"
            }
        ],
        "active":true,
        "name":{
            "family":"Franco Ballen",
            "given":"Fabian Alejandro",
            "prefix":null
        },
        "telecom":[
            {
                "system":"phone",
                "value":"3132423927",
                "use":"mobile"
            },
            {
                "system":"phone",
                "value":"6019413574",
                "use":"home"
            }
        ],
        "gender":"M",
        "birthDate":"2005-11-18"
    }
    """
    aleDict = json.loads(aleJson)
    aleP=Patient(aleDict)
    aleP.guardarEnBaseDeDatos()