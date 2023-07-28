import logging
import os
import pandas as pd
import json


class DatasetCreator:
    """
    Class for convenient work with source data
    """

    def __init__(self, data_path: str):
        """
        init method
        :param data_path: path to source directory with docs
        """
        self.data_path = data_path
        self.epicrysis_files = []
        self.results_files = []
        for _, _, filenames in os.walk(data_path):
            for filename in filenames:
                match filename:
                    case _ if filename.endswith('xml'):
                        self.epicrysis_files.append(filename[:-4])
                    case _ if filename.endswith('json'):
                        self.results_files.append(filename[:-12])
                    case _:
                        logging.error(f'File not recognized {filename}')

    def get_file_names(self) -> tuple:
        """
        just return two lists
        :return: (epicrysis_files, result_files)
        """
        return sorted(list(set(self.epicrysis_files).intersection(set(self.results_files))))

    def get_me_dataset(self) -> pd.DataFrame:
        """
        method for dtaset creation
        :return:
        """
        all_results = []
        for filename in self.get_file_names():
            with open('../dataset_tutorial/' + filename + '_result.json', 'r', encoding='utf8') as fh:
                results = json.load(fh)
                for i, result in enumerate(results):
                    results[i]['filename'] = filename + '.xml'
                all_results.extend(results)

        df = pd.DataFrame(data=all_results)
        df.drop(columns=['id', 'code'], inplace=True)
        return df
