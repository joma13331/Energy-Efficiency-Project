import os
import numpy as np
import pandas as pd
from EElogging.EELogger import EELogger
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler


class EEFeatureEngineeringPred:
    """
        :Class Name: EEFeatureEngineeringPred
        :Description: This class is used to modify the dataframe while performing data
                      preprocessing

        Written By: Jobin Mathew
        Interning at iNeuron Intelligence
        Version: 1.0
    """

    def __init__(self):
        """
        :Method Name: __init__
        :Description: This method is Constructor for class EEFeatureEngineeringTrain.
                      Initializes variables for logging
        """
        self.logger = EELogger()
        if not os.path.isdir("EElogging/prediction/"):
            os.mkdir("EElogging/prediction/")
        self.log_path = "EElogging/prediction/EEFeatureEngineeringPred.txt"

    def ee_standard_scaling_features(self, dataframe):
        """
        :Method Name: ee_standard_scaling_features
        :Description: This method takes in a dataframe and scales it using standard scalar
        :param dataframe: this is the dataframe that needs to be scaled
        :return: The Scaled dataset.
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')
            scaler = StandardScaler()
            scaled_df = pd.DataFrame(scaler.fit_transform(dataframe), columns=dataframe.columns)
            message = "The dataset has been scaled using Standard Scalar"
            self.logger.log(log_file, message)
            log_file.close()
            return scaler, scaled_df

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while trying to scale data: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_handling_missing_data_mcar(self, dataframe, feature_with_missing):
        try:
            log_file = open(self.log_path, 'a+')
            dropped_features = []
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            for feature in feature_with_missing:
                if dataframe[feature].isna().mean > 0.75:
                    dataframe.drop(columns=feature)
                    dropped_features.append(feature)
                    message = f" Dropped {feature} as more than 75% values are missing"
                    self.logger.log(log_file, message)

                else:
                    dataframe[feature + 'nan'] = np.where(dataframe[feature].isnull(), 1, 0)

            data = imputer.fit_transform(dataframe)
            dataframe = pd.DataFrame(data=data, columns=dataframe.columns)

            message = f" missing values imputed using KNNImputer for {list(set(feature_with_missing).symmetric_difference(set(dropped_features)))}"
            self.logger.log(log_file, message)

            log_file.close()
            return dataframe, imputer, dropped_features

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while trying to handle missing data due to mcar: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
