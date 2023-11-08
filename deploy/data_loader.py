import os
import pandas as pd

class DataLoader:
    def __init__(self, data_directory):
        self.data_directory = data_directory
        self.dataframes = {}

    def load_data(self):
        files = os.listdir(self.data_directory)
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(self.data_directory, file)
                dataframe_name = os.path.splitext(file)[0]
                self.dataframes[dataframe_name] = pd.read_csv(file_path)

    def get_dataframes(self):
        return self.dataframes

