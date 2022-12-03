from utils import *
from requests.request import Request

DEFAULT_TEMPLATE_PATH = r'src\api\requests\templates\conditional_formatting_between.json'

class IsBetween(Request):
    def __init__(self, sheet_id, start_column_index, end_column_index, start_row_index, end_row_index, 
                    lower_bound, upper_bound, color, template_path=DEFAULT_TEMPLATE_PATH,):
        self.sheet_id = sheet_id
        self.start_column_index = start_column_index
        self.end_column_index = end_column_index
        self.start_row_index = start_row_index
        self.end_row_index = end_row_index
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.color = get_color_rgb(color)
        self.template_path = template_path

    def get_sheet_id(self):
        return self.sheet_id

    def get_start_column_index(self):
        return self.start_column_index

    def get_end_column_index(self):
        return self.end_column_index

    def get_start_row_index(self):
        return self.start_row_index

    def get_end_row_index(self):
        return self.end_row_index

    def get_lower_bound(self):
        return self.lower_bound

    def get_upper_bound(self):
        return self.upper_bound

    def get_color(self):
        # In RGB
        return self.color

    def get_dict_attrs(self):
        return {
            'SHEET_ID': self.sheet_id,
            'START_COLUMN_INDEX': self.start_column_index,
            'END_COLUMN_INDEX': self.end_column_index,
            'START_ROW_INDEX': self.start_row_index,
            'END_ROW_INDEX': self.end_row_index,
            'LOWER_BOUND': self.lower_bound,
            'UPPER_BOUND': self.upper_bound,
            'RED': self.color['red'],
            'GREEN': self.color['green'],
            'BLUE': self.color['blue']
        }