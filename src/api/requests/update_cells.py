from requests.request import Request

DEFAULT_TEMPLATE_PATH = r'src\api\requests\templates\updateCells.json'

class UpdateCells(Request):
    def __init__(self, sheet_id, start_column_index, end_column_index,
                 start_row_index, end_row_index, template_path=DEFAULT_TEMPLATE_PATH):
        self.sheet_id = sheet_id
        self.start_column_index = start_column_index
        self.end_column_index = end_column_index
        self.start_row_index = start_row_index
        self.end_row_index = end_row_index
        super().__init__(template_path)

    def get_dict_attrs(self):
        return {
            'SHEET_ID': self.sheet_id,
            'START_COLUMN_INDEX': self.start_column_index,
            'END_COLUMN_INDEX': self.end_column_index,
            'START_ROW_INDEX': self.start_row_index,
            'END_ROW_INDEX': self.end_row_index,
        }