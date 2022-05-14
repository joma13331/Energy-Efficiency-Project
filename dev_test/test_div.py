from Training.EEDataFormatTrain import EEDataFormatTrain

test_obj = EEDataFormatTrain("../TrainDatasets/")
obj_length, obj_col_names, obj_col_Num = test_obj.ee_values_from_schema()
print(obj_length, obj_col_names, obj_col_Num)
obj_regex = test_obj.ee_regex_file_name()
print(obj_regex)
test_obj.ee_delete_existing_good_data_folder()
test_obj.ee_delete_existing_bad_data_folder()
test_obj.ee_create_good_bad_raw_data_directory()
test_obj.ee_validating_file_name(obj_regex)
test_obj.ee_validate_column_length(obj_col_Num)