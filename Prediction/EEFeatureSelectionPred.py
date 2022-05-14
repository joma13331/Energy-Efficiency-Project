import os
from EElogging.EELogger import EELogger


class EEFeatureSelectionPred:
    """
        :Class Name: EEFeatureSelectionPred
        :Description: This class is used to select the features that will be sent for
                      clustering

        Written By: Jobin Mathew
        Interning at iNeuron Intelligence
        Version: 1.0
        """

    def __init__(self):
        """
        :Method Name: __init__
        :Description: This method is Constructor for class EEFeatureSelectionTrain.
                      Initializes variables for logging
        """
        self.logger = EELogger()
        if not os.path.isdir("EElogging/prediction/"):
            os.mkdir("EElogging/prediction/")
        self.log_path = "EElogging/prediction/EEFeatureSelectionPred.txt"

    def ee_remove_columns(self, dataframe, columns):
        """
        :Method Name: ee_remove_columns
        :Description: This method is used to delete columns from a pandas dataframe.

        :param dataframe: The pandas dataframe from which the columns have to be
                          removed.
        :param columns: The columns that have to be removed.
        :return: A pandas dataframe with the columns removed.
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')
            dataframe = dataframe.drop(columns=columns)
            message = f"The following columns were dropped: {columns}"
            self.logger.log(log_file, message)
            log_file.close()
            return dataframe

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while deleting columns: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

