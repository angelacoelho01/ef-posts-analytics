from requests.request import Request

DEFAULT_TEMPLATE_PATH = r'src\api\requests\templates\addSheet.json'
CELL_RANGE = 'A1:Z999'

class AddSheet(Request):
    def __init__(self, sheet_name, template_path=DEFAULT_TEMPLATE_PATH):
        self.sheet_name = sheet_name
        self.values = []
        self.template_path = template_path

    def get_sheet_name(self):
        return self.sheet_name

    def get_dict_attrs(self):
        return {
            'SHEET_NAME': self.sheet_name
        }
    
    def get_values(self):
        return self.values
    
    def set_values(self, values):
        self.values = values

    def add_values(self, values):
        self.values = self.values + values

    def update_sheet(self, service, spreadsheet_id, all_sheets):
        # Check if sheet already exists in the spreadsheet
        if (self.sheet_name not in all_sheets):
            self.send_request(service, spreadsheet_id)
            
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption='USER_ENTERED',
            range=self.sheet_name + "!" + CELL_RANGE,
            body={
                'majorDimension': 'ROWS',
                'values': self.get_values()
            }
        ).execute()