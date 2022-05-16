import os
import pandas as pd
from EElogging.EELogger import EELogger


class EEDataLoaderPred:
    """
    :Class Name: EEDataLoaderTrain
    :Description: This class contains the method for loading the training data into
                  a pandas dataframe for future usage

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """
    def __init__(self):
        self.training_file = 'prediction_file.csv'
        self.logger = EELogger()
        if not os.path.isdir("EElogging/prediction/"):
            os.mkdir("EElogging/prediction/")
        self.log_path = "EElogging/prediction/EEDataLoaderPred.txt"

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
            message = "The prediction data is loaded successfully as a pandas dataframe"
            self.logger.log(log_file, message)
            log_file.close()
            return self.data

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while trying to load the data for prediction to pandas dataframe: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

