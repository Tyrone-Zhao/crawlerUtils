import csv


__all__ = ["writeCsv", "readCsv"]


def writeCsv(row=None, dict_params=None, fieldnames=None, filepath=None,
             writer=None, mode="w", newline="", encoding="utf-8-sig", *args, **kwargs):
    ''' 写csv文件 '''
    if filepath != None and fieldnames == None:
        with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
            writer = csv.writer(f)
        return writer
    elif filepath != None and fieldnames != None:
        with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        return writer
    if writer != None and row != None:
        writer.writerow(row)
        return writer
    if writer != None and dict_params != None:
        writer.writerow(dict_params)
        return writer


def readCsv(filepath=None, isDictReader=False, mode="r", newline="", encoding="utf-8-sig", *args, **kwargs):
    ''' 读取csv文件 '''
    if isDictReader:
        with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
            reader = csv.DictReader(f)
            return reader
    else:
        with open(filepath, mode, newline=newline, encoding=encoding, *args, **kwargs) as f:
            reader = csv.reader(f)
            return reader