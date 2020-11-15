import json

class JsonDebugger:
    
    def __init__(self, response):
        self.json_response = response.json()

    '''
    Idented json for better visualisation
    '''
    def debug(self):
        self.json_str = json.dumps(self.json_response)
        self.json_object = json.loads(self.json_str)
        print(json.dumps(self.json_object, indent = 3))
