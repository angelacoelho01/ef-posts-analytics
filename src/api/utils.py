import matplotlib.colors

ENCODING = 'latin-1'

def get_color_rgb(color_hex):
    color_rgb = matplotlib.colors.to_rgb(color_hex)
    return {
        'red': str(color_rgb[0]),
        'green': str(color_rgb[1]),
        'blue': str(color_rgb[2])
    }

# Source code found in: https://stackoverflow.com/questions/55704719/python-replace-values-in-nested-dictionary
def dict_replace_value(d, old, new):
    x = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = dict_replace_value(v, old, new)
        elif isinstance(v, list):
            v = list_replace_value(v, old, new)
        elif isinstance(v, str):
            v = v.replace(old, new)
        x[k] = v
    return x

def list_replace_value(l, old, new):
    x = []
    for e in l:
        if isinstance(e, list):
            e = list_replace_value(e, old, new)
        elif isinstance(e, dict):
            e = dict_replace_value(e, old, new)
        elif isinstance(e, str):
            e = e.replace(old, new)
        x.append(e)
    return x


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
