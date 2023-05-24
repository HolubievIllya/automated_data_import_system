import pandas as pd


def read_excel_columnames(path: str) -> list:
    file = pd.read_excel(path)
    return file.columns.values


def read_column_by_colname(path: str, colname: str):
    file = pd.read_excel(path)
    return [i for i in file[colname].tolist() if i >= 0]
