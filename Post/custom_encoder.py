
#CustomEncoder is designed to check if an instanced passed to it is a decimal
#(Since values retured ny the DynamoDB are of Decimal Form) and convert it into float

import json
from decimal import Decimal


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj , Decimal):
            return float(obj)
        
        return json.JSONEncoder.default(self ,obj)
            
    