import json
from utils import *
from requests.request import Request

DEFAULT_TEMPLATE_PATH = r'src\api\requests\templates\add_sheet.json'

class AddSheet(Request):
    def __init__(self, sheet_name, template_path=DEFAULT_TEMPLATE_PATH):
        self.sheet_name = sheet_name
        self.template_path = template_path

    def get_sheet_name(self):
        return self.sheet_name

    def get_dict_attrs(self):
        return {
            'SHEET_NAME': self.sheet_name
        }