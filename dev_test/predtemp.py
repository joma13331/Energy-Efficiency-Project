"""from Prediction.EEDataInjestionCompTrain import EEDataInjestionCompPred
from Prediction.EEDataFormat import EEDataFormatPred
from Prediction.EEBeforeUploadTrain import EEBeforeUploadPred
from Prediction.EEDBOperationTrain import EEDBOperationPred

data_format = EEDataFormatPred("../PredDatasets/")
regex = data_format.ee_regex_file_name()
data_format.ee_validating_file_name(regex)
length_year_of_file, column_names, column_number = data_format.ee_values_from_schema()
data_format.ee_validate_column_length(column_number)
data_format.ee_validate_whole_columns_as_empty()

data_transformer = EEBeforeUploadPred()
data_transformer.ee_replace_missing_with_null()

db_operator = EEDBOperationPred()
#db_operator.ee_create_table(column_names)

#db_operator.ee_insert_good_pred_data()

data_format.ee_delete_existing_good_data_folder()
data_format.ee_move_bad_files_to_archive()
db_operator.ee_data_from_db_to_csv()"""

"""from Prediction.EEDataLoaderTrain import EEDataLoaderTrain
from Prediction.EE_EDA import EEPredEda
from Prediction.EEFeatureEngineeringTrain import EEFeatureEngineeringPred
from Prediction.EEFeatureSelectionTrain import EEFeatureSelectionPred
from FileOperations.EEFileOperations import EEFileOperation
import pandas as pd

data_loader = EEDataLoaderTrain()
prediction_data = data_loader.ee_get_data()
# print(prediction_data)

eda = EEPredEda()
feature_engineer = EEFeatureEngineeringPred()
feature_selector = EEFeatureSelectionPred()
file_operator = EEFileOperation()

inputs = feature_selector.ee_remove_columns(prediction_data, 'id')
# print(prediction_data)
# print(inputs)

features = [inputs, inputs]

for j in range(2):

    with open(f"../column_to_drop_y{j + 1}.txt", 'r') as f:
        val = f.read()

    col_to_drop = val.split(",")

    features[j] = feature_selector.ee_remove_columns(features[j], col_to_drop)
    scalar = file_operator.ee_load_model("../Models/scalar.pickle")
    features[j] = pd.DataFrame(data=scalar.transform(features[j]), columns=features[j].columns)

    kmeans = file_operator.ee_load_model(f"../Models/Clustering/clustering_model_y{j+1}.pickle")

    features[j]["clusters"] = kmeans.predict(features[j])
    features[j]['id'] = prediction_data['id']
    result = []
    for i in features[j]["clusters"].unique():
        cluster_data = features[j][features[j]["clusters"] == i]
        id = cluster_data['id']
        cluster_data = cluster_data.drop(columns=["clusters", 'id'])
        model = file_operator.ee_load_ml_model(j + 1, i)
        pred_result = list(model.predict(cluster_data))
        result.extend(list(zip(id, pred_result)))

    res_dataframe = pd.DataFrame(data=result, columns=["id", f'y{j}'])
    prediction_data = prediction_data.merge(right=res_dataframe, on='id', how='outer')
prediction_data.to_csv("../prediction_result.csv", header=True, index=False)"""

from Prediction.EEPredictionPipeline import EEPredictionPipeline
from Prediction.EEDataInjestionCompPred import EEDataInjestionCompPred
pipeline = EEPredictionPipeline()

data_injection = EEDataInjestionCompPred("../Uploaded_Files/")
data_injection.ee_data_injestion_complete()
#dataformatter = EEDataFormatPred("../Uploaded_Files/ENB2022_data.xlsx")
#dataformatter.ee_convert_direct_excel_to_csv()

json_result = pipeline.ee_predict()

for record in json_result:
    print(record)
