import json
import os

import pandas as pd

from EElogging.EELogger import EELogger
from EEFileOperations.EEFileOperations import EEFileOperation
from EEPrediction.EEDataLoaderPred import EEDataLoaderPred
from EEPrediction.EEEDAPred import EEPredEda
from EEPrediction.EEFeatureEngineeringPred import EEFeatureEngineeringPred
from EEPrediction.EEFeatureSelectionPred import EEFeatureSelectionPred


class EEPredictionPipeline:

    def __init__(self):
        if not os.path.isdir("EElogging/prediction/"):
            os.mkdir("EElogging/prediction/")
        self.log_path = "EElogging/prediction//EEPredictionPipeline.txt"
        self.logger = EELogger()
        self.model_dir = "EEModels/EEMlmodels/"
        self.cluster_dir = "EEModels/EEClustering/"

    def ee_predict(self):
        try:
            log_file = open(self.log_path, 'a+')
            message = "Start of EEPrediction Pipeline"
            self.logger.log(log_file, message)

            # GETTING THE DATA
            data_loader = EEDataLoaderPred()
            prediction_data = data_loader.ee_get_data()

            message = f"EEPrediction data obtained"
            self.logger.log(log_file, message)

            # DATA PROCESSING
            message = f"Data Preprocessing started"
            self.logger.log(log_file, message)

            eda = EEPredEda()
            feature_engineer = EEFeatureEngineeringPred()
            feature_selector = EEFeatureSelectionPred()
            file_operator = EEFileOperation()

            inputs = feature_selector.ee_remove_columns(prediction_data, 'ID')

            is_null_present, columns_with_null = eda.ee_missing_values(inputs)

            if is_null_present:
                inputs, imputer, dropped_features = feature_engineer.ee_handling_missing_data_mcar(inputs,
                                                                                                   columns_with_null)

            features = [inputs, inputs]

            for j in range(2):

                with open(f"column_to_drop_Y{j + 1}.txt", 'r') as f:
                    val = f.read()

                col_to_drop = val.split(",")

                features[j] = feature_selector.ee_remove_columns(features[j], col_to_drop)
                scalar = file_operator.ee_load_model("EEModels/scalar.pickle")
                features[j] = pd.DataFrame(data=scalar.transform(features[j]), columns=features[j].columns)

                kmeans = file_operator.ee_load_model(f"EEModels/EEClustering/clustering_model_Y{j + 1}.pickle")

                features[j]["clusters"] = kmeans.predict(features[j])
                features[j]['ID'] = prediction_data['ID']
                result = []
                for i in features[j]["clusters"].unique():
                    cluster_data = features[j][features[j]["clusters"] == i]
                    id = cluster_data['ID']
                    cluster_data = cluster_data.drop(columns=["clusters", 'ID'])
                    model = file_operator.ee_load_ml_model(j + 1, i)
                    pred_result = list(model.predict(cluster_data))
                    result.extend(list(zip(id, pred_result)))

                res_dataframe = pd.DataFrame(data=result, columns=["ID", f'Y{j + 1}'])
                prediction_data = prediction_data.merge(right=res_dataframe, on='ID', how='outer')
            prediction_data = prediction_data.round(2)
            prediction_data = prediction_data.drop(columns=["ID"])
            prediction_data.to_csv("prediction_result.csv", header=True, index=False)

            message = "End of EEPrediction Pipeline"
            self.logger.log(log_file, message)

            return json.loads(prediction_data.to_json(orient="records"))

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"Error while trying to scale data: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
