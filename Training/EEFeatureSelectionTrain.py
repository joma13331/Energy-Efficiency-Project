import os
import pandas as pd
from EElogging.EELogger import EELogger
from sklearn.feature_selection import mutual_info_regression


class EEFeatureSelectionTrain:
    """
        :Class Name: EEFeatureSelectionTrain
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
        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")
        self.log_path = "EElogging/training/EEFeatureSelectionTrain.txt"

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

    def ee_col_with_high_correlation(self, dataframe, threshold=0.8):
        """
        :Method Name: ee_col_with_high_correlation
        :Description: This method finds out those features which can be removed to remove multi-collinearity.

        :param dataframe: The pandas dataframe to check for features with multi-collinearity
        :param threshold: The threshold above which features are taken to be collinear
        :return: A list of features that can be dropped to remove multi-collinearity
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            col_corr = set()  # Set of all the names of correlated columns
            corr_matrix = dataframe.corr()
            for i in range(len(corr_matrix.columns)):
                for j in range(i):
                    if abs(corr_matrix.iloc[i, j]) > threshold:  # we are interested in absolute coeff value
                        colname = corr_matrix.columns[i]  # getting the name of column
                        col_corr.add(colname)

            message = f" The following columns have high correlation with other columns {str(col_corr)}"
            self.logger.log(log_file, message)
            log_file.close()
            return list(col_corr)

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while detecting collinear columns in features: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_feature_not_important(self, features, label, threshold=0.1):
        """
        :Method Name: ee_feature_not_important
        :Description: This method determined those features which are not important to determine the output label

        :param features: The input features of the dataset provided by the client
        :param label: The output label being considered for determining feature to drop
        :param threshold: the value below which if columns have value they can be removed
        :return: A list of features that can be dropped as they have no impact on output label
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            mutual_info = mutual_info_regression(features, label)
            feature_imp = pd.Series(mutual_info, index=features.columns)
            not_imp = list(feature_imp[feature_imp < threshold].index)

            message = f"The features which have no or very impact on the output are {not_imp}"
            self.logger.log(log_file, message)
            log_file.close()

            return not_imp

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while detecting columns in features with no impact on output: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_features_with_zero_std(self, dataframe):
        """
        :Method Name: ee_features_with_zero_std
        :Description: This method checks whether any of the columns of the passed
                      dataframe has all values as equal and returns a list of all such
                      columns

        :param dataframe: The pandas dataframe to check for columns with all values as same
        :return: list of columns with zero std
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')
            columns_zero_std = []

            for feature in dataframe.columns:
                if dataframe[feature].std() == 0:
                    columns_zero_std.append(feature)

            message = f"the features with all values as equal are {columns_zero_std}"
            self.logger.log(log_file, message)
            log_file.close()

            return columns_zero_std

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while detecting columns all values as equal: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
