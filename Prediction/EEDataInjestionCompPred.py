import pandas as pd
import threading
from Prediction.EEDataFormatPred import EEDataFormatPred
from Prediction.EEDBOperationPred import EEDBOperationPred
from Prediction.EEBeforeUploadPred import EEBeforeUploadPred
from EElogging.EELogger import EELogger
import os


class EEDataInjestionCompPred:
    """
    :Class Name: EEDataInjestionCompPred
    :Description: This class utilized 3 Different classes
                    1. EEDataFormatValPred
                    2. EEBeforeUploadPred
                    3. EEDBOperationPred
                  to complete validation on the dataset names, columns, etc based on
                  the DSA with the client. It then uploads the valid files to a cassandra
                  Database. Finally it obtains a csv from the database to be used further
                  for preprocessing and training

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """

    def __init__(self, path="PredDatasets/"):
        self.data_format_validator = EEDataFormatPred(path=path)
        self.db_operator = EEDBOperationPred()
        self.data_transformer = EEBeforeUploadPred()
        self.logger = EELogger()
        if not os.path.isdir("EElogging/prediction/"):
            os.mkdir("EElogging/prediction/")
        self.log_path = "EElogging/prediction/EEDataInjestionCompPred.txt"

    def ee_data_injestion_complete(self):
        """
        :Method Name: ee_data_injestion_complete
        :Description: This method is used to complete the entire data validation,
                      data injestion process to store the data in a database and
                      convert it for further usage in our project work

        :return: None
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')
            message = "Start of Injestion and Validation"
            self.logger.log(log_file, message)

            filename_length, dataset_col_names, dataset_col_num = self.data_format_validator.ee_values_from_schema()
            regex = self.data_format_validator.ee_regex_file_name()
            self.data_format_validator.ee_validating_file_name(regex)
            self.data_format_validator.ee_validate_column_length(dataset_col_num)
            self.data_format_validator.ee_validate_whole_columns_as_empty()

            message = "Raw Prediction Data Validation complete"
            self.logger.log(log_file, message)

            message = "Start of Data Transformation"
            self.logger.log(log_file, message)

            self.data_transformer.ee_replace_missing_with_null()

            message = "Data Transformation Complete"
            self.logger.log(log_file, message)

            message = "Start of upload of the Good Prediction Data to Cassandra Database"
            self.logger.log(log_file, message)

            # Threading used to bypass time consuming database tasks to improve web application latency.
            t1 = threading.Thread(target=self.db_operator.ee_complete_db_pipeline,
                                  args=[dataset_col_names, self.data_format_validator])
            t1.start()

            self.data_format_validator.ee_convert_direct_excel_to_csv()
            # t1 not joined so that it runs only after prediction has occurred.

            message = "End of upload of the Good Prediction Data to Cassandra Database"
            self.logger.log(log_file, message)

            message = "End of Injestion and Validation"
            self.logger.log(log_file, message)

            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error During Injestion and Validation Phase{str(e)}"
            self.logger.log(log_file, message)
            raise e
