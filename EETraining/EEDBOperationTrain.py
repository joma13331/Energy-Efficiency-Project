
import os
import cassandra
from cassandra.query import dict_factory
import pandas as pd

from EElogging.EELogger import EELogger
import csv
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class EEDBOperationTrain:
    """
    This class will handle all the relevant operations related to Cassandra Database.

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """

    def __init__(self):
        """
        :Method Name: __init__
        :Description: This constructor initializes the variable that will be utilized
                      in all the class methods
        """
        self.logger = EELogger()
        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")
        self.log_path = "EElogging/training/EEDBOperationTrain.txt"
        self.good_file_dir = "EEDIV/ValidatedData/GoodRaw/"
        self.bad_file_dir = "EEDIV/ValidatedData/BadRaw/"
        self.table_name = "good_data"

    def ee_db_connection(self):
        """
        :Method Name: ee_db_connection
        :Description: This method connects to the keyspace used for storing the validated
                      good dataset for this work.
        :return: session which is a cassandra database connection
        :On Failure: cassandra.cluster.NoHostAvailable, Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            cloud_config = {
                'secure_connect_bundle': 'secure-connect-ineuron.zip'
            }
            auth_provider = PlainTextAuthProvider(os.getenv('CASSANDRA_CLIENT_ID'),
                                                  os.getenv('CASSANDRA_CLIENT_SECRET'))
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

            session = cluster.connect()
            session.row_factory = dict_factory
            message = "Connection successful with cassandra database"
            self.logger.log(log_file, message)

            session.execute("USE energy_efficiency_internship;")

            message = "accessed the energy_efficiency_internship keyspace"
            self.logger.log(log_file, message)

            log_file.close()

            return session

        except cassandra.cluster.NoHostAvailable:
            log_file = open(self.log_path, 'a+')
            message = "Connection Unsuccessful with cassandra database due to Incorrect credentials or no connection from" \
                      "datastax"
            self.logger.log(log_file, message)
            log_file.close()
            raise cassandra.cluster.NoHostAvailable
        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Connection Unsuccessful with cassandra database: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_create_table(self, column_names):
        """
        :Method Name: ee_create_table
        :Description: This method created a 'good_data' table to store good data
                      with the appropriate column names.
        :param column_names: Column Names as expected from EESchema based on DSA
        :return:None
        :On Failure: Exception
        """

        try:
            log_file = open(self.log_path, 'a+')
            session = self.ee_db_connection()

            table_creation_query = f"CREATE TABLE IF NOT EXISTS {self.table_name}(id int primary key,"
            for col_name in column_names:
                table_creation_query += f"{col_name} {column_names[col_name]},"
            # table_creation_query[:-1] is used to not consider the ',' at the end.
            table_creation_query = table_creation_query[:-1] + ");"
            session.execute(table_creation_query)
            message = "The table for Good Data created"
            self.logger.log(log_file, message)

            session.execute(f"truncate table {self.table_name};")
            message = "Any row if existing deleted"
            self.logger.log(log_file, message)
            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"The table for Good Data was Not created: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

        finally:
            try:
                session.shutdown()
                log_file = open(self.log_path, 'a+')
                message = f"Session terminated create table operation"
                self.logger.log(log_file, message)
                log_file.close()

            except Exception as e:
                pass

    def ee_insert_good_data(self):
        """
        :Method Name: ee_insert_good_data
        :Description: This method uploads all the files in the good Data folder
                      to the good_data table in cassandra database.
        :return: None
        :On Failure: Exception
        """
        try:

            count = 0
            col_names = "ID,"
            session = self.ee_db_connection()

            for filename in os.listdir(self.good_file_dir):
                temp_df = pd.read_excel(os.path.join(self.good_file_dir, filename))

                # count variable is used so the the column part of the query is created only once as it is same for all
                # the insertion queries
                if count == 0:
                    for i in list(temp_df.columns):
                        col_names += f"{i},"
                    # col_names[:-1] is used to not consider the ',' at the end
                    col_names = col_names[:-1]
                    count += 1

                # the for loop creates the values to be uploaded.
                # it is complicated to ensure that any 'null' value in a string column is entered as null and not a
                # simple string.
                for i in range(len(temp_df)):
                    # [i] is the value for id.

                    temp_lis = [i] + list(temp_df.iloc[i])
                    if 'null' in temp_lis:
                        tup = "("
                        for j in temp_lis:
                            if type(j) == str:
                                if j == 'null':
                                    tup += f"{j},"
                                else:
                                    tup += f"'{j}',"
                            else:
                                tup += f"{j},"
                        tup = tup[:-1] + ")"
                    else:
                        tup = tuple(temp_lis)
                    insert_query = f"INSERT INTO good_data({col_names}) VALUES {tup};"
                    print(insert_query)
                    session.execute(insert_query)

                log_file = open(self.log_path, "a+")
                message = f"Data in {filename} uploaded successfully to good_data table"
                self.logger.log(log_file, message)
                log_file.close()

        except Exception as e:
            log_file = open(self.log_path, "a+")
            message = f"Error while uploading data to good_data table: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

        finally:
            try:
                session.shutdown()
                log_file = open(self.log_path, 'a+')
                message = f"Session terminated insert data operation"
                self.logger.log(log_file, message)
                log_file.close()

            except Exception as e:
                pass

    def ee_data_from_db_to_csv(self):
        """
        :Method Name: ee_data_from_db_to_csv
        :Description: This method downloads all the good data from the cassandra
                      database to a csv file for preprocessing and training.
        :return: None
        :On Failure: Exception
        """
        try:
            session = self.ee_db_connection()
            validated_data_file = 'validated_file.csv'
            col_name_query = "select column_name from system_schema.columns where " \
                             "keyspace_name='energy_efficiency_internship' and table_name='good_data'; "
            headers = []
            result = session.execute(col_name_query)
            for i in result:
                # upper is used as in the original files it is expected that it will be in upper case
                headers.append(str(i['column_name']).upper())
                print(i['column_name'])

            get_all_data_query = "select * from good_data;"
            results = session.execute(get_all_data_query)
            data = []

            for result in results:
                row = []
                for header in headers:
                    # lower() because cassandra database converts all column names to lower case.
                    row.append(result[header.lower()])
                data.append(row)

            with open(validated_data_file, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(headers)
                csv_writer.writerows(data)

            log_file = open(self.log_path, 'a+')
            message = f"All data from good data table saved to {validated_data_file}"
            self.logger.log(log_file, message)
            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while downloading good data into csv file: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

        finally:
            try:
                session.shutdown()
                log_file = open(self.log_path, 'a+')
                message = f"Session terminated after downloading good data into csv file from table{self.table_name}"
                self.logger.log(log_file, message)
                log_file.close()

            except Exception as e:
                pass

    def ee_complete_db_pipeline(self, column_names, data_format_validator):
        """
        :Method Name: ee_complete_db_pipeline
        :Description: This methods is written so that it can be run on a background thread to make ensure our web app
                      first makes the prediction to ensure less latency.
                      Only after the prediction is displayed on the web app does the database operations begin.
        :param column_names: The column names of the table in the cassandra database.
        :param data_format_validator: An object of EEDataFormatPred class to perform deletion and transfer of files
        :return: None
        :On Failure: Exception
        """
        try:
            self.ee_create_table(column_names=column_names)
            self.ee_insert_good_data()
            data_format_validator.ee_delete_existing_good_data_folder()
            data_format_validator.ee_move_bad_files_to_archive()
            self.ee_data_from_db_to_csv()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while downloading good data into csv file: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
