from datetime import datetime
import os
import cassandra
from cassandra.query import dict_factory
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


class EELogger:
    """
    :Class Name: EMLogger
    : Description: EMLogger is a helper class designed to write logs to a local file.
                   It has one method "log" which writes the given message to a txt file.
                   It is expected to be modified to write messages to a cassandra database depending on latency.

    Written by: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """

    def log(self, file_obj, log_message):
        """
        :Method Name: log
        :Description: This method writes the passed message to the file object passed as parameters.
                      Important for keeping proper records of all relevant events.
        :param file_obj: The file object to write the message to
        :param log_message: The message to be written.
        :return: None
        """
        now = datetime.now()
        date = now.date()
        cur_time = now.strftime("%H:%M:%S")
        file_obj.write(
            f"{str(date)}/{str(cur_time)}\t\t {log_message}\n"
        )

    def ee_db_connection(self):
        """
        :Method Name: ee_db_connection
        :Description: This method connects to the keyspace used for storing the log messages for this work.
        :return: session which is a cassandra database connection
        :On Failure: cassandra.cluster.NoHostAvailable, Exception
        """

        cloud_config = {
            'secure_connect_bundle': "../secure-connect-ineuron.zip"
        }
        auth_provider = PlainTextAuthProvider(os.getenv('CASSANDRA_CLIENT_ID'),
                                              os.getenv('CASSANDRA_CLIENT_SECRET'))
        cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)

        session = cluster.connect()
        session.row_factory = dict_factory
        session.execute("USE energy_efficiency_internship;")

        return session

    def ee_log_to_database(self, table_name, message):

        session = self.ee_db_connection()

        table_creation_query = f"CREATE TABLE IF NOT EXISTS {table_name}(id uuid primary key, message_time timestamp, " \
                               f"message text); "
        session.execute(table_creation_query)
        table_entry_query = f"INSERT INTO {table_name}(id, message_time, message) VALUES(now(), toTimestamp(now()), '{message}'); "
        session.execute(table_entry_query)

        session.shutdown()

    def ee_obtain_logs_from_database(self, table_name):

        session = self.ee_db_connection()

        table_select_query = f"SELECT * from {table_name};"
        results = session.execute(table_select_query)

        messages = []
        for result in results:
            row = [result['id'], result['message_time'], result['message']]
            messages.append(row)

        session.shutdown()

        return messages




