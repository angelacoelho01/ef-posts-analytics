from requests.add_sheet import AddSheet

CELL_RANGE = 'A1:Z999'

class Sheet:
    def __init__(self, name):
        self.name = name
        self.values = []

    def get_name(self):
        return self.name

    def get_values(self):
        return self.values

    def set_values(self, values):
        self.values = values

    def add_sheet(self, service, spreadsheet_id):
        return AddSheet(self.name).send_request(service, spreadsheet_id)

    def update_sheet(self, service, spreadsheet_id):
        self.add_sheet(service, spreadsheet_id)
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            valueInputOption='USER_ENTERED',
            range=self.name + '!' + CELL_RANGE,
            body={
                'majorDimension': 'ROWS',
                'values': self.get_values()
            }
        ).execute()
