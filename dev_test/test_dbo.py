from Training.EEBeforeUploadTrain import EEBeforeUploadTrain
# test_obj = EEDataFormatTrain("../TrainDatasets/")
# obj_length, obj_col_names, obj_col_Num = test_obj.ee_values_from_schema()

# obj_dbop = EEDBOperationTrain()
# obj_dbop.ee_create_table(obj_col_names)
# obj_dbop.ee_insert_good_data()

# obj_dbop.ee_db_connection()

obj_dt = EEBeforeUploadTrain()
obj_dt.ee_replace_missing_with_null()