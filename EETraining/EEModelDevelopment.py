import os

from sklearn.model_selection import train_test_split
from EETraining.EEDataLoaderTrain import EEDataLoaderTrain
from EETraining.EEEDATrain import EEEdaTrain
from EETraining.EEFeatureEngineeringTrain import EEFeatureEngineeringTrain
from EETraining.EEFeatureSelectionTrain import EEFeatureSelectionTrain
from EETraining.EEClusteringTrain import EEClusteringTrain
from EETraining.EEModelFinder import EEModelFinder
from EElogging.EELogger import EELogger
from EEFileOperations.EEFileOperations import EEFileOperation


class EETrainingPipeline:

    def __init__(self):

        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")
        self.log_path = "EElogging/training/EETrainingPipeline.txt"
        self.logger = EELogger()

        if not os.path.isdir("EEModels/EEMlmodels/"):
            os.mkdir("EEModels/EEMlmodels/")
        self.model_dir = "EEModels/EEMlmodels/"

        if not os.path.isdir("EEModels/EEClustering/"):
            os.mkdir("EEModels/EEClustering/")
        self.cluster_dir = "EEModels/EEClustering/"

    def ee_model_train(self):

        try:
            log_file = open(self.log_path, 'a+')
            message = "Start of EETraining Pipeline"
            self.logger.log(log_file, message)

            # GETTING THE DATA
            data_loader = EEDataLoaderTrain()
            validated_data = data_loader.ee_get_data()

            message = f"Validated data obtained"
            self.logger.log(log_file, message)

            # DATA PROCESSING

            message = f"Data Preprocessing started"
            self.logger.log(log_file, message)

            eda = EEEdaTrain()
            feature_engineer = EEFeatureEngineeringTrain()
            feature_selector = EEFeatureSelectionTrain()
            file_operator = EEFileOperation()

            temp_df = feature_selector.ee_remove_columns(validated_data, 'ID')

            features, labels = eda.ee_feature_label_split(temp_df, ['Y1', 'Y2'])

            # features is a list of same features as the only elements. This is because we have two outputs.
            for j in range(len(features)):
                is_null_present, columns_with_null = eda.ee_missing_values(features[j])

                if is_null_present:
                    features[j], imputer, dropped_features = feature_engineer.ee_handling_missing_data_mcar(features[j],
                                                                                                            columns_with_null)

                col_to_drop = feature_selector.ee_features_with_zero_std(features[j])
                col_to_drop.extend(feature_selector.ee_feature_not_important(features[j], labels[j]))
                col_to_drop.extend(feature_selector.ee_col_with_high_correlation(features[j]))

                print(col_to_drop)

                col_to_drop = list(set(col_to_drop))
                col_to_drop_str = ",".join(col_to_drop)

                with open(f"column_to_drop_Y{j+1}.txt", 'w') as f:
                    f.write(col_to_drop_str)

                features[j] = feature_selector.ee_remove_columns(features[j], col_to_drop)

                scalar, features[j] = feature_engineer.ee_standard_scaling_features(features[j])

                file_operator.ee_save_model(scalar, "EEModels/", "scalar.pickle")

                message = f"Data Preprocessing completed"
                self.logger.log(log_file, message)

                # CLUSTERING

                message = f"clustering of dataset started"
                self.logger.log(log_file, message)

                cluster = EEClusteringTrain()
                num_clusters = cluster.ee_obtain_optimum_cluster(features[j])
                cluster_model, features[j] = cluster.ee_create_cluster(features[j], num_clusters)

                file_operator.ee_save_model(cluster_model, self.cluster_dir, f"clustering_model_Y{j+1}.pickle")
                features[j]['labels'] = labels[j]

                list_of_clusters = features[j]['cluster'].unique()

                message = f"clustering of dataset done"
                self.logger.log(log_file, message)

                for i in list_of_clusters:
                    message = f"Start of training for output Y{j+1} cluster{i}"
                    self.logger.log(log_file, message)

                    cluster_data = features[j][features[j]['cluster'] == i]

                    cluster_feature = cluster_data.drop(columns=['labels', 'cluster'])
                    cluster_label = cluster_data['labels']

                    train_x, test_x, train_y, test_y = train_test_split(cluster_feature, cluster_label, random_state=42)
                    model_finder = EEModelFinder()
                    model_name, model = model_finder.ee_best_model(train_x=train_x, train_y=train_y,
                                                                   test_x=test_x, test_y=test_y)

                    file_operator.ee_save_model(model=model, model_dir=self.model_dir,
                                                model_name=f"{model_name}_Y{j+1}_cluster_{i}.pickle")

                    message = f"Model for cluster {i} trained"
                    self.logger.log(log_file, message)

            message = "Successful End of EETraining"
            self.logger.log(log_file, message)
            log_file.close()

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while obtaining best model: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e
