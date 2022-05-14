import os
import re
import json
import shutil
import pandas as pd
from datetime import datetime
from EElogging.EELogger import EELogger


class EEDataFormatTrain:
    """
    Class Name: EEDataFormatTrain
    Description: This class shall be used for handling all the validation done on the Raw Training Data

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """
    def __init__(self, path):
        """
        :Method Name: __init__
        :Description: The constructor of class EEDataFormatTrain
        :param path: path to the datasets folder(xlsx)
        """
        self.dir_path = path
        self.good_raw_path = "DIV/ValidatedData/GoodRaw/"
        self.bad_raw_path = "DIV/ValidatedData/BadRaw/"
        self.schema_path = "schema/training_schema.json"

        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")

        self.log_path = "EElogging/training/EEDataFormatTrain.txt"

        self.logger = EELogger()

    def ee_values_from_schema(self):
        """
        :Method Name: ee_values_from_schema
        :Description: This method utilizes the training file schema from DSA to obtain
                      the expected dataset filename and dataset column details.
        :On Failure: can Raise ValueError, KeyError or Exception
        :return: 1. length of the Year that should be in filename
                 2. column names and corresponding datatype
                 3. Number of Columns expected in the dataset
        """
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)

            length_year_of_file = dic["LengthOfYear"]
            column_names = dic["ColumnNames"]
            column_number = dic["NumberOfColumns"]
            # If in any of the above the values on the RHS is not Equal to no of variables in LHS ValueError is Raised
            # If any of the above key is absent in schema_training.json then KeyError is raised

            log_file = open(self.log_path, "a+")
            message = f"Length of year of file = {length_year_of_file}, Number of columns = {column_number}"
            self.logger.log(log_file, message)
            log_file.close()

            return length_year_of_file, column_names, column_number

        except ValueError:
            log_file = open(self.log_path, "a+")
            message = "ValueError:Value not found inside schema_training.json"
            self.logger.log(log_file, message)
            log_file.close()
            raise ValueError

        except KeyError:
            log_file = open(self.log_path, "a+")
            message = "KeyError:Incorrect key passed for schema_training.json"
            self.logger.log(log_file, message)
            log_file.close()
            raise KeyError

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            self.logger.log(log_file, str(e))
            log_file.close()
            raise e

    def ee_regex_file_name(self):
        """
        Method Name: ee_regex_file_name
        Description: To generate the regex to compare whether the filename is
                     according to the DSA or not
        :return: Required Regex pattern
        :On Failure: None
        """
        regex = re.compile(r'ENB[1,2]\d{3}_data.xlsx')
        return regex

    def ee_create_good_bad_raw_data_directory(self):
        """
        :Method Name: ee_create_good_bad_raw_data_directory
        :Description: This method creates directories to store the Good Data and Bad Data
                      after validating the training data.
        :return: None
        On Failure: OSError
        """
        try:

            if not os.path.isdir(self.good_raw_path):
                os.makedirs(self.good_raw_path)
            if not os.path.isdir(self.bad_raw_path):
                os.makedirs(self.bad_raw_path)

            log_file = open(self.log_path, 'a+')
            message = f"Good and Bad file directory created"
            self.logger.log(log_file, message)
            log_file.close()

        except OSError as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while creating directory: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise OSError

    def ee_delete_existing_good_data_folder(self):
        """
        :Method Name: ee_delete_existing_good_data_folder
        :Description: This method deletes the directory made to store the Good Data
                      after loading the data in the table. Once the good files are
                      loaded in the DB,deleting the directory ensures space optimization.
        :return: None
        :On Failure: OSError
        """

        try:

            if os.path.isdir(self.good_raw_path):
                shutil.rmtree(self.good_raw_path)
                log_file = open(self.log_path, 'a+')
                message = "GoodRaw directory deleted successfully!!!"
                self.logger.log(log_file, message)
                log_file.close()
        except OSError as e:
            log_file = open("../EElogging/file_validation/data_validation_segregation.txt", 'a+')
            message = f"Error while Deleting Directory: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_delete_existing_bad_data_folder(self):
        """
                :Method Name: ee_delete_existing_bad_data_folder
                :Description: This method deletes the directory made to store the Bad Data
                              after moving the data in an archive folder. We archive the bad
                              files to send them back to the client for invalid data issue.
                :return: None
                :On Failure: OSError
                """
        try:

            if os.path.isdir(self.bad_raw_path):
                shutil.rmtree(self.bad_raw_path)
                log_file = open(self.log_path, 'a+')
                message = "BadRaw directory deleted successfully!!!"
                self.logger.log(log_file, message)
                log_file.close()
        except OSError as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while Deleting Directory: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_move_bad_files_to_archive(self):
        """
        :Method Name: ee_move_bad_files_to_archive
        Description: This method deletes the directory made to store the Bad Data
                      after moving the data in an archive folder. We archive the bad
                      files to send them back to the client for invalid data issue.
        :return: None
        : On Failure: Exception
        """
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H_%M_%S")

        try:

            if os.path.isdir(self.bad_raw_path):
                archive_dir = "DIV/ArchivedData"
                if not os.path.isdir(archive_dir):
                    os.makedirs(archive_dir)
                archive_path = os.path.join(archive_dir, f"BadData_{str(date)}_{time}")
                bad_files = os.listdir(self.bad_raw_path)
                for file in bad_files:
                    if file not in os.listdir(archive_path):
                        shutil.move(self.bad_raw_path+file, archive_path)
                log_file = open(self.log_path, "a+")
                message = f"Bad files moved to archive: {archive_path}"
                self.logger.log(log_file, message)
                log_file.close()
                self.ee_delete_existing_bad_data_folder()
        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while Archiving Bad Files: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_validating_file_name(self, regex):
        """
        :Method Name:
        :Description: This function validates the name of the training xlsx files as per given name in the schema!
                      Regex pattern is used to do the validation.If name format do not match the file is moved
                      to Bad Raw Data folder else in Good raw data.
        :param regex: The regex compiler used to check validity of filenames
        :return: None
        :On Failure: Exception
        """

        # delete the directories for good and bad data in case last run was unsuccessful and folders were not deleted.
        self.ee_delete_existing_bad_data_folder()
        self.ee_delete_existing_good_data_folder()
        # create new directories
        self.ee_create_good_bad_raw_data_directory()
        raw_files = [file for file in os.listdir(self.dir_path)]

        try:
            log_file = open(self.log_path, 'a+')
            for filename in raw_files:
                if re.match(regex, filename):
                    shutil.copy(os.path.join(self.dir_path, filename), self.good_raw_path)
                    message = f"{filename} is valid!! moved to GoodRaw folder"
                    self.logger.log(log_file, message)
                else:
                    shutil.copy(os.path.join(self.dir_path, filename), self.bad_raw_path)
                    message = f"{filename} is not valid!! moved to BadRaw folder"
                    self.logger.log(log_file, message)
            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error occurred while validating filename: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_validate_column_length(self, number_of_columns):
        """
        :Method Name: ee_validate_column_length
        :Description: This function validates the number of columns in the csv files.
                       It is should be same as given in the schema file.
                       If not same file is not suitable for processing and thus is moved to Bad Raw Data folder.
                       If the column number matches, file is kept in Good Raw Data for processing.

        :param number_of_columns: The number of columns that is expected based on DSA
        :return: None
        :On Failure: OSERROR, EXCEPTION
        """
        try:
            log_file = open(self.log_path, 'a+')
            message = "Column Length Validation Started!!"
            self.logger.log(log_file, message)
            for filename in os.listdir(self.good_raw_path):
                pd_df = pd.read_excel(os.path.join(self.good_raw_path, filename))

                # Accessing the number of columns in the relevant files by checking shape of the dataframe.
                if not pd_df.shape[1] == number_of_columns:
                    shutil.move(os.path.join(self.good_raw_path, filename), self.bad_raw_path)
                    message = f"invalid Column length for the file {filename}. File moved to Bad Folder"
                    self.logger.log(log_file, message)
                else:
                    message = f"{filename} validated. File remains in Good Folder"
                    self.logger.log(log_file, message)
            self.logger.log(log_file, "Column Length Validation Completed!!")
            log_file.close()
        except OSError:
            log_file = open(self.log_path, 'a+')
            message = f"Error occurred when moving the file: {str(OSError)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise OSError
        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error occurred : {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_validate_whole_columns_as_empty(self):

        try:
            log_file = open(self.log_path, 'a+')
            message = "Missing Values Validation Started!!"
            self.logger.log(log_file, message)
            for filename in os.listdir(self.good_raw_path):
                pd_df = pd.read_excel(os.path.join(self.good_raw_path, filename))
                for column in pd_df:
                    if (len(pd_df[column]) - pd_df[column].count()) == len(pd_df[column]):
                        shutil.move(os.path.join(self.good_raw_path, filename), self.bad_raw_path)
                        message = f"invalid column {column}. Moving to Bad Folder"
                        self.logger.log(log_file, message)
                        break
        except OSError:
            log_file = open(self.log_path, 'a+')
            message = f"Error occurred when moving the file: {str(OSError)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise OSError
        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error occurred : {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_convert_direct_excel_to_csv(self):
        """
        :Method Name: ee_convert_direct_excel_to_csv
        :Description: This function converts all the excel files which have been validated as being in the correct
                      format into a single csv file which is then used in preprocessing for training ML Models.
                      This function is used to improve the speed or latency of the web application as the app does not
                      have to wait for database operations before starting the training.
        :return: None
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            list_pd = []
            for filename in os.listdir(self.good_raw_path):
                list_pd.append(pd.read_excel(os.path.join(self.good_raw_path, filename)))

            df = pd.concat(list_pd)

            df.to_csv("validated_file.csv", header=True, index=True, index_label="ID")

            message = f"Excel file Converted directly to required csv file for future preprocessing"
            self.logger.log(log_file, message)
            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error occurred while direct conversion from excel to csv: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
