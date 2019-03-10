import xlrd
import xlwt


__all__ = [
    "Excel",
]


class Excel():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def excelWrite(self, row=None, column=None, label=None, worksheet=None, workbook=None, sheetname=None,
                encoding="ascii"):
        """ 写入Excel, 从0开始 """
        ws = None
        if workbook:
            wb = workbook
        else:
            wb = xlwt.Workbook(encoding=encoding)
        if worksheet:
            ws = worksheet
        elif sheetname:
            ws = wb.add_sheet(sheetname)

        if row != None and column != None and label != None and ws:
            ws.write(row, column, label=label)

        if ws:
            return ws
        else:
            return wb


    @classmethod
    def excelRead(self, excelpath=None, cell_row_num=None, cell_column_num=None,
                row_num=None, column_num=None, sheetindex=0, sheetname=None,
                workbook=None, worksheet=None, nrows=False, ncols=False):
        """ 读取Excel, 行数和列数从0开始，单元格也从0开始 """
        if workbook and sheetname:
            ws = workbook.sheet_by_name(sheetname)
            return ws
        elif workbook and sheetindex:
            ws = workbook.sheet_by_index(sheetindex)
            return ws
        elif workbook:
            wb = workbook
        elif excelpath:
            wb = xlrd.open_workbook(excelpath)
        elif worksheet:
            ws = worksheet
        else:
            raise ValueError("缺少Excel路径或Excel对象，或者Sheet对象！")

        if not sheetindex and not sheetname:
            ws = wb.sheet_by_index(0)

        if nrows:
            return ws.nrows
        elif ncols:
            return ws.ncols

        if cell_row_num != None and cell_column_num != None:
            return ws.cell(cell_row_num, cell_column_num).value
        elif row_num != None:
            return ws.row_values(row_num)
        elif column_num != None:
            return ws.col_values(column_num)

        return wb.sheets()
