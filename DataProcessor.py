import pandas as pd

class DataProcessor:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_data(self):
        return self.data

    def clean_data(self):
        # Example: drop NaN rows
        self.data.dropna(inplace=True)
        return self.data
