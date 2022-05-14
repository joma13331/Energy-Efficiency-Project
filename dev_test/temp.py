# from DataModeling.EEDataLoaderTrain import EEDataLoaderTrain
# from DataModeling.EE_EDA import EEEdaTrain
# from DataModeling.EEFeatureEngineeringTrain import EEFeatureEngineeringTrain
# from DataModeling.EEFeatureSelectionTrain import EEFeatureSelectionTrain
# from DataModeling.EEClusteringTrain import EEClusteringTrain
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from MLModel.EEModelFinder import EEModelFinder
#
# dataloader = EEDataLoaderTrain()
# dataframe = dataloader.ee_get_data()
#
# # print(dataframe)
#
# eda = EEEdaTrain()
# feature_engineer = EEFeatureEngineeringTrain()
# feature_selector = EEFeatureSelectionTrain()
#
# temp_df = feature_selector.ee_remove_columns(dataframe, 'id')
# # print(temp_df)
#
# features, labels = eda.ee_feature_label_split(temp_df, ['y1', 'y2'])
# print(len(features))
# print(len(labels))
#
# is_null_present, columns_with_null = eda.ee_missing_values(features[0])
# # print(is_null_present, columns_with_null)
#
# col_to_drop = feature_selector.ee_features_with_zero_std(features[0])
# col_to_drop.extend(feature_selector.ee_feature_not_important(features[0], labels[0]))
# col_to_drop.extend(feature_selector.ee_col_with_high_correlation(features[0]))
#
# col_to_drop = list(set(col_to_drop))
# # print(col_to_drop)
#
# features[0] = feature_selector.ee_remove_columns(features[0], col_to_drop)
#
# #print(features[0])
#
# scaler, features[0] = feature_engineer.ee_standard_scaling_features(features[0])
# # print(features[0])
#
# cluster = EEClusteringTrain()
# num_clusters = cluster.ee_obtain_optimum_cluster(features[0])
# features[0] = cluster.ee_create_cluster(features[0], num_clusters)
#
# # print(num_clusters, features[0])
#
# features[0]['labels'] = labels[0]
# # print(features[0])
#
# list_of_clusters = features[0]['cluster'].unique()
# # print(list_of_clusters)
#
# cluster_data = features[0][features[0]['cluster'] == 1]
# # print(len(cluster_data))
#
# cluster_feature = cluster_data.drop(columns=['labels', 'cluster'])
# cluster_label = cluster_data['labels']
# #print(cluster_feature, cluster_label)
#
# train_x, test_x, train_y, test_y = train_test_split(cluster_feature, cluster_label, random_state=42)
# model_finder = EEModelFinder()
#
# model_name, model = model_finder.ee_best_model(train_x=train_x, train_y=train_y, test_x=test_x, test_y=test_y)
# print(model_name, model_finder.ee_adj_r2(model, train_x, train_y))
# print(model_name, model_finder.ee_adj_r2(model, test_x, test_y))

from Training.EEModelDevelopment import EETrainingPipeline
#from DBOp.EEDBOperationTrain import EEDBOperationTrain
train_pipeline = EETrainingPipeline()
train_pipeline.ee_model_train()

#db_operator = EEDBOperationTrain()
#db_operator.ee_data_from_db_to_csv()
