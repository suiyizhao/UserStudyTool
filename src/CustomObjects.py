import os
import json
import xlwt
from xlwt import Workbook
from PyQt5.QtWidgets import QFileDialog

from CustomFuncs import sort_by_key

class Task():
    def __init__(self, root_path, num_methods, num_imgs, cur_index, rated_list, unrated_list, auto_next, displayed_scale, displayed_column, result_dict):
        self.save_path = ''
        self.root_path = root_path
        self.num_methods = num_methods
        self.num_imgs = num_imgs
        self.cur_index = cur_index
        self.rated_list = rated_list
        self.unrated_list = unrated_list
        self.auto_next = auto_next
        self.displayed_scale = displayed_scale
        self.displayed_column = displayed_column
        self.result_dict = result_dict

    # def setSavePath(self, save_path):
    #     self.save_path = save_path

    # def setCurIndex(self, cur_index):
    #     self.cur_index = cur_index

    # def setRatedList(self, rated_list):
    #     self.rated_list = rated_list

    # def setUnratedList(self, unrated_list):
    #     self.unrated_list = unrated_list

    # def setDisplayedScale(self, displayed_scale):
    #     self.displayed_scale = displayed_scale

    # def setDisplayedColumn(self, displayed_column):
    #     self.displayed_column = displayed_column
    
    def save(self):
        self.result_dict = dict(sort_by_key(self.result_dict))
        if self.save_path == '':
            file_name = QFileDialog.getSaveFileName(None, 'Save File', 'task.json', 'JSON Files (*.json)')
            self.save_path = file_name[0]
            if file_name[0]:
                with open(file_name[0], 'w', encoding='utf-8') as f:
                    json.dump(self.__dict__, f, ensure_ascii=False, indent=4) 
        else:
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

    def load(self, name):
        pass

class TableWriter(Workbook):
    def __init__(self, root_path):
        super().__init__()

        self.root_path = root_path
        methods = sorted(os.listdir(self.root_path))
        self.columns = len(methods) + 1
        self.rows = len(os.listdir(os.path.join(self.root_path, methods[0]))) + 2

        self.table = self.add_sheet('sheet1', cell_overwrite_ok=True)

        # Set style for table head
        self.style_head = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        font.name = 'Times New Roman'
        self.style_head.font = font

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        self.style_head.alignment = alignment

        # Set style for table body
        self.style_body = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = False
        font.name = 'Times New Roman'
        self.style_body.font = font

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        self.style_body.alignment = alignment

        # Set style for table tail
        self.style_tail = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        font.colour_index = xlwt.Style.colour_map['red']
        font.name = 'Times New Roman'
        self.style_tail.font = font

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        self.style_tail.alignment = alignment
        
        # Initialize the table
        self.table.write(0, 0, 'ith', self.style_head)
        for j in range(1, self.columns):
            self.table.write(0, j, methods[j-1], self.style_head)
        for i in range(1, self.rows-1):
            self.table.write(i, 0, i, self.style_body)
        self.table.write(self.rows-1, 0, 'Vote', self.style_tail)   
        
    def writeTable(self, row, column, value, is_body=True):
        if is_body:
            self.table.write(row, column, value, style = self.style_body)
        else:
            self.table.write(row, column, value, style = self.style_tail)

    def saveTable(self):
        file_name = QFileDialog.getSaveFileName(None, 'Save File', 'result.xls', 'Excel Files (*.xls)')
        if file_name[0] != '':
            self.save(file_name[0])