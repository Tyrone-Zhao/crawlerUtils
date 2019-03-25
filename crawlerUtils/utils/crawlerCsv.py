import csv


__all__ = ["Csv"]


class Csv():

    def __init__(self, **kwargs):
        super().__init__()

    @classmethod
    def csvWrite(self, row=None, dict_params=None, fieldnames=None, filepath=None,
                writer=None, mode="w", newline="", encoding="utf-8-sig", *args, **kwargs):
        ''' 写csv文件 '''
        if filepath != None and fieldnames == None and row == None:
            with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
                writer = csv.writer(f)
        elif filepath != None and fieldnames != None and dict_params is None:
            with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
        if filepath != None and row != None:
            with open(filepath, "a", newline=newline, encoding=encoding, *args, **kwargs) as f:
                writer = csv.writer(f)
                writer.writerow(row)
        if filepath != None and dict_params != None:
            with open(filepath, "a", newline=newline, encoding=encoding, *args, **kwargs) as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writerow(dict_params)


    @classmethod
    def csvRead(self, filepath=None, isDictReader=False, mode="r", newline="", encoding="utf-8-sig", *args, **kwargs):
        ''' 读取csv文件 '''
        if isDictReader:
            with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
                reader = csv.DictReader(f)
                return reader
        else:
            with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
                reader = csv.reader(f)
                return reader