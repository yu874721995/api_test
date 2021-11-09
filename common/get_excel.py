# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/4/9 17:42
# @File      : get_excel.py
# @SoftWare  : dengta_api_test

import xlrd


class get_excel(object):

    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.file = xlrd.open_workbook(self.file_path)
        try:
            self.sheet = self.file.sheet_by_index(self.sheet_name)
        except Exception as e:
            self.sheet = self.file.sheet_by_name(self.sheet_name)

    def get_oneColum(self, col, types=None):
        '''返回一列中所有单元格的数据'''
        col -= 1
        if types == 'values':  # 数据
            return self.sheet.col_values(col, start_rowx=0, end_rowx=None)
        elif types == 'types':  # 数据类型
            return self.sheet.col_types(col, start_rowx=0, end_rowx=None)
        elif types == 'slice':  # 对象
            return self.sheet.col_slice(col, start_rowx=0, end_rowx=None)
        elif types is None:  # 同slice
            return self.sheet.col(col, start_rowx=0, end_rowx=None)
        else:
            return self.sheet.col(col, start_rowx=0, end_rowx=None)

    def get_oneRow(self, col, types=None):
        '''返回一行中所有单元格的数据'''
        col -= 1
        if types == 'values':  # 数据
            return self.sheet.row_values(col, start_rowx=0, end_rowx=None)
        elif types == 'types':  # 数据类型
            return self.sheet.row_types(col, start_rowx=0, end_rowx=None)
        elif types == 'slice':  # 对象
            return self.sheet.row_slice(col, start_rowx=0, end_rowx=None)
        elif types is None:  # 同slice
            return self.sheet.row(col, start_rowx=0, end_rowx=None)
        else:
            return self.sheet.row(col, start_rowx=0, end_rowx=None)

    def get_oneCell(self, row, col, types=None):
        '''返回单元格中的数据'''
        row -= 1
        col -= 1
        if types == 'values':  # 数据
            return self.sheet.cell_value(col, start_rowx=0, end_rowx=None)
        elif types == 'types':  # 数据类型
            return self.sheet.cell_type(col, start_rowx=0, end_rowx=None)
        elif types == 'slice':  # 对象
            return self.sheet.cell_slice(col, start_rowx=0, end_rowx=None)
        elif types is None:  # 同slice
            return self.sheet.cell(col, start_rowx=0, end_rowx=None)
        else:
            return self.sheet.cell_xf_index(col, start_rowx=0, end_rowx=None)
