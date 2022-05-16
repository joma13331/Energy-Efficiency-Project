import pandas as pd
import os
from EElogging.EELogger import EELogger


class EEEdaTrain:
    """
    :Class Name: EEEdaTrain
    :Description: This class is used to explore the data given by the client and come
                 to some conclusion about the data.

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """

    def __init__(self):
        """
        :Method Name: __init__
        :Description: This method is Constructor for class EEEdaTrain.
                      Initializes variables for logging
        """
        self.logger = EELogger()
        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")
        self.log_path = "EElogging/training/EEEdaTrain.txt"

    def ee_feature_label_split(self, dataframe, label_col_names):
        """
        :Method Name: ee_feature_label_split
        :Description: This method splits the features and labels from the validated
                      dataset and returns them

        :param dataframe: The pandas dataframe to obtain features and labels from
        :param label_col_names: the name of label columns
        :return: features - a pandas dataframe composed of all the features
                 labels - a dictionary composed of all labels as key and corresponding
                          pandas dataseries as value.
        :On Failure: Exception
        """

        try:
            log_file = open(self.log_path, 'a+')

            features = dataframe.drop(columns=label_col_names)
            labels = dataframe[label_col_names]

            message = "The features and labels were obtained from the dataset"
            self.logger.log(log_file, message)
            log_file.close()
            return [features, features], [labels['Y1'], labels['Y2']]

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while obtaining feature and labels: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_missing_values(self, dataframe):
        """
        :Method Name: ee_missing_values
        :Description: This method finds out whether there are missing values in the
                      validated data and returns a list of feature names with missing
                      values

        :param dataframe: the Dataframe in which features with missing values are
                          required to be found
        :return: missing_val_flag - whether the dataframe has missing values or not
                 features_with_missing - If missing values are present then list of
                 columns with missing values otherwise an empty list
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            features_with_missing = [feature for feature in dataframe.columns if dataframe[feature].isna().sum() > 0]
            missing_val_flag = False
            if len(features_with_missing) > 0:
                missing_val_flag = True

            message = f"There are {len(features_with_missing)} features with missing values"
            self.logger.log(log_file, message)
            log_file.close()

            return missing_val_flag, features_with_missing

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while detecting columns with missing values: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e





