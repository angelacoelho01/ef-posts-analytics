import json
from utils import *

class Request:
    def __init__(self, template_path):
        self.template_path = template_path

    def get_template_path(self):
        return self.get_template_path

    def get_dict_attrs(self):
        pass

    def get_request_body(self):
        with open(self.template_path, 'r+') as json_template:
            request_body = json.load(json_template)
 
            for field, value in self.get_dict_attrs().items():
                request_body = dict_replace_value(request_body, field, str(value))

            return request_body

    def send_request(self, service, spreadsheet_id):
        self.get_request_body()
        try:
            response = service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=self.get_request_body()
            ).execute()

            return response
        except Exception as e:
            print(e)