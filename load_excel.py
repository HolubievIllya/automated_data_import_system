import pandas as pd


def read_excel_columnames(path: str) -> list:
    file = pd.read_excel(path)
    # print(file.columns.values)
    return file.columns.values

def read_column_by_colname(path:str, colname: str):
    file = pd.read_excel(path)
    # print(file[colname].tolist())
    # print([i for i in file[colname].tolist() if i >= 0])
    return [i for i in file[colname].tolist() if i >= 0]

# print(read_excel_columnames("Лист Microsoft Excel.xlsx")[0])
# print(read_column_by_colname("Лист Microsoft Excel.xlsx", read_excel_columnames("Лист Microsoft Excel.xlsx")[0]))