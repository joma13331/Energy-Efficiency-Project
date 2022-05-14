import os
import pandas as pd
from EElogging.EELogger import EELogger


class EEDataLoaderTrain:
    """
    :Class Name: EEDataLoaderTrain
    :Description: This class contains the method for loading the training data into
                  a pandas dataframe for future usage

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """
    def __init__(self):
        self.training_file = "validated_file.csv"
        self.logger = EELogger()
        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")
        self.log_path = "EElogging/training/EEDataLoaderTrain.txt"

    def ee_get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception
        """
        try:
            log_file = open(self.log_path, 'a+')
            self.data = pd.read_csv(self.training_file)
            # To round all the values to two decimal digits as it is usually in the data files.
            self.data = self.data.round(2)
            message = "The training data is loaded successfully as a pandas dataframe"
            self.logger.log(log_file, message)
            log_file.close()
            return self.data

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while trying to load the data for training to pandas dataframe: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

