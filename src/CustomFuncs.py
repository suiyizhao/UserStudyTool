import sys
import math

def index2point(index, column):
    '''
    E.g., column:3
    index:0 --> (0,0)
    index:5 --> (1,2)
    index:7 --> (2,1)
    index:13 --> (4,1)
    '''
    return (math.floor(index/column), index%column)

def point2index(point, column):
    '''
    E.g., column:3
    point:(0,0) --> 0
    point:(1,2) --> 5
    point:(2,1) --> 7
    point:(4,1) --> 13
    '''
    return point[0]*column+point[1]

def is_invaild_scale(scale):
    '''
    Judge if a given scale is invaild.
    E.g.,
    scale:'0.1,0.5' --> False
    scale:'0.1,0.' --> True 
    scale:'0.1,0' --> True 
    scale:'0.1,' --> True 
    scale:'0.1' --> True 
    '''
    splitted = scale.split(',')
    if len(splitted) != 2:
        return True
    else:
        if splitted[1] == '':
            return True
        elif float(splitted[1]) < 0.1:
            return True
        else:
            return False

def sort_by_key(dict):
    '''
    E.g.:
    Given: {'a': 2018, 'z': 2019, 'b': 2017}
    Return: [('a', 2018), ('b', 2017), ('z', 2019)]
    dict(Return): {'a': 2018, 'b': 2017, 'z': 2019}
    '''
    return sorted(dict.items(), key=lambda k: k[0])

def get_max_less_than_x(x, ordered_list):
    '''
    E.g.:
    Given: x: 13  ordered_list: [3, 4, 5, 6, 8, 9, 10, 13, 14, 15]
    Return: 10
    '''
    for v in ordered_list[::-1]:
        if v < x:
            return v
    return x

def get_min_more_than_x(x, ordered_list):
    '''
    E.g.:
    Given: x: 13  ordered_list: [3, 4, 5, 6, 8, 9, 10, 13, 14, 15]
    Return: 14
    '''
    for v in ordered_list:
        if v > x:
            return v
    return x

def check_path(path):
    '''
    Used to avoid path errors after the application is packaged using pyinstall --onefile
    E.g.:
    Given: path: './ui/MainWindow.ui'
    if it's a packaged executable
        return: 'sys._MEIPASS/ui/MainWindow.ui'
    if it's a raw Python script
        return: './ui/MainWindow.ui'
    '''
    if getattr(sys, 'frozen', False):
        # If it's a packaged executable, not a a raw Python script
        path = sys._MEIPASS + path[1:]

    return path