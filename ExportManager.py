import pandas as pd

class ExportManager:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def to_csv(self, file_name="output.csv"):
        self.data.to_csv(file_name, index=False)
        return file_name

    def to_excel(self, file_name="output.xlsx"):
        self.data.to_excel(file_name, index=False)
        return file_name
