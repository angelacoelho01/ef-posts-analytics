ENCODING = 'latin-1'

def add_sheets(service, google_sheet_id, sheet_name):
    try:
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }]
        }

        response = service.spreadsheets().batchUpdate(
            spreadsheetId=google_sheet_id,
            body=request_body
        ).execute()

        return response
    except Exception as e:
        print(e)

def add_conditional_formatting_rules(service, sheet_id):
    try:
        request_body = {
            'requests': [{
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{
                            'sheetId': 2021327580,
                            'startColumnIndex': 3,
                            'endColumnIndex': 4,
                            'startRowIndex': 0,
                            'endRowIndex': 300
                        }],
                        'booleanRule': {
                            'condition': {
                                'type': 'NUMBER_BETWEEN',
                                'values': [{
                                    'userEnteredValue': '0'
                                }, {
                                    'userEnteredValue': '200'
                                }]
                            },
                            'format': {
                                'backgroundColor': {
                                    'red': 0.95,
                                    'green': 0.8,
                                    'blue': 0.8
                                }
                            }
                        }
                    },
                    'index': 0
                }
            }]
        }

        response = service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body=request_body
        ).execute()

        return response
    except Exception as e:
        print(e)