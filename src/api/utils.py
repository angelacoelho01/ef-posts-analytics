import matplotlib.colors
import numpy as np

ENCODING = 'latin-1'

# Colors
EXTREMLY_GOOD = '#bdd6ee'
VERY_GOOD = '#c5e0b3'
GOOD = '#ffe599'
COULD_BE_BETTER = '#f6b26b'
BELOW_EXPECTATIONS = '#ea9999'

COLORS = [
    BELOW_EXPECTATIONS,
    COULD_BE_BETTER,
    GOOD,
    VERY_GOOD,
    EXTREMLY_GOOD
]

def get_outliers(data):
    outliers=[]
    
    threshold=3
    mean = np.mean(data)
    std =np.std(data)
    
    
    for y in data:
        z_score= (y - mean)/std 
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers

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


def get_values_from_dataset(df):
    values = []

    values.append(list(df.columns.values))
    #views_col = list(df.columns.values).index('Visualizações')
    
    df.reset_index()
    num_col = 0
    for _, row in df.iterrows():
        values.append(list(row))
        num_col += 1

    return values

def get_q1(min, mean):
    return (mean - min)//2

def get_q3(mean, max):
    return (max - mean)//2
