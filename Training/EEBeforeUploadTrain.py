import os
import pandas as pd
from EElogging.EELogger import EELogger


class EEBeforeUploadTrain:
    """
    :Class Name: EEBeforeUploadTrain
    :Description: This class is used to transform the Good Raw Files before uploading to
                  to cassandra database

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """
    def __init__(self):

        self.logger = EELogger()
        # setting up the instance variable where the acceptable files for training are present.
        self.good_raw_path = "DIV/ValidatedData/GoodRaw/"

        # setting up the instance variable for the path of file where relevant logs will be stored.
        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")
        self.log_path = "EElogging/training/EEBeforeUploadTrain.txt"

    def ee_replace_missing_with_null(self):
        """
        :Method Name: ee_replace_missing_with_null
        :Description: This method replaces all the missing values with 'null'.
        :return: None
        :On Failure: Exception
        """

        try:

            log_file = open(self.log_path, 'a+')

            # Find all the files in the acceptable files folder and fill 'null' wherever there are missing values.
            # 'null' is being used so that cassandra database can accept missing values even in numerical columns.
            for filename in os.listdir(self.good_raw_path):
                temp_df = pd.read_excel(os.path.join(self.good_raw_path, filename))
                temp_df.fillna('null', inplace=True)
                temp_df.to_excel(os.path.join(self.good_raw_path, filename), header=True, index=None)
                message = f"{filename} transformed successfully"
                self.logger.log(log_file, message)
                log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Data Transformation Failed: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
