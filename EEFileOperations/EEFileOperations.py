import pickle
import os
import shutil
from EElogging.EELogger import EELogger


class EEFileOperation:
    """
    This class shall be used to save the model after training
    and load the saved model for prediction.

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0

    """

    def __init__(self):

        self.logger = EELogger()

        if not os.path.isdir("EElogging/"):
            os.mkdir("EElogging/")

        self.log_path = "EElogging/file_operations.txt"

    def ee_save_model(self, model, model_dir, model_name):
        """
        :Method Name: ee_save_model
        :Description: This method saves the passed model to the given directory

        :param model: The sklearn model to save.
        :param model_dir: The folder/directory where model need to be stored
        :param model_name: the name of the model
        :return: None
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            path = os.path.join(model_dir, model_name)
            if not os.path.isdir(model_dir):
                os.makedirs(model_dir)

            with open(path, 'wb') as f:
                pickle.dump(model, f)

            message = f"{model_name} has been save in {model_dir}"
            self.logger.log(log_file, message)
            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while save {model_name} in {model_dir}: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_load_model(self, model_path):
        """
        :Method Name: ee_load_model
        :Description: This method is used to obtain the model stored at the given file path.

        :param model_path: The path where model is stored.
        :return: The model stored at the passed path.
        :On Failure: Exception
        """

        try:
            log_file = open(self.log_path, 'a+')

            f = open(model_path, 'rb')
            model = pickle.load(f)
            message = f"model at {model_path} loaded successfully"
            self.logger.log(log_file, message)

            log_file.close()
            return model

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while loading model at {model_path}: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_load_ml_model(self, output_no, cluster_no):
        try:
            log_file = open(self.log_path, 'a+')

            model_dir = "EEModels/EEMlmodels/"
            for filename in os.listdir(model_dir):
                if filename.endswith(f"_Y{output_no}_cluster_{cluster_no}.pickle"):
                    message = f"file: {filename} selected for prediction"
                    self.logger.log(log_file, message)
                    return self.ee_load_model(os.path.join(model_dir, filename))

            message = "No Model Found"
            self.logger.log(log_file, message)

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while trying to retrieve data: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
