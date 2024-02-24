from CrossValidation import CrossValidation
import os

origin_folder = "arff_datasets"
destination_folder = "arff_datasets_folds"
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

for file in os.listdir(origin_folder):
        if file.endswith(".arff"):
            print(file)
            CV = CrossValidation(os.path.join(os.path.abspath(origin_folder),file),distance_func="default",file_type="arff")

            SCV_folds,SCV_folds_y,SCV_folds_inx=CV.SCV(foldNum=5)

            DBSCV_folds,DBSCV_folds_y,DBSCV_folds_inx=CV.DBSCV(foldNum=5)

            MSSCV_folds,MSSCV_folds_y,MSSCV_folds_inx=CV.MSSCV(foldNum=5)

            DOBSCV_folds,DOBSCV_folds_y,DOBSCV_folds_inx=CV.DOBSCV(foldNum=5)

            paht_output = os.path.join(os.path.abspath(destination_folder),file.split(".")[0])
            if not os.path.exists(paht_output+"-SCV"):
                os.makedirs(paht_output+"-SCV")
            CV.write_folds(SCV_folds,SCV_folds_y,file.split(".")[0]+"-SCV",paht_output+"-SCV/")

            if not os.path.exists(paht_output+"-DBSCV"):
                os.makedirs(paht_output+"-DBSCV")
            CV.write_folds(DBSCV_folds,DBSCV_folds_y,file.split(".")[0]+"-DBSCV",paht_output+"-DBSCV/")

            if not os.path.exists(paht_output+"-MSSCV"):
                os.makedirs(paht_output+"-MSSCV")
            CV.write_folds(MSSCV_folds,MSSCV_folds_y,file.split(".")[0]+"-MSSCV",paht_output+"-MSSCV/")

            if not os.path.exists(paht_output+"-DOBSCV"):
                os.makedirs(paht_output+"-DOBSCV")
            CV.write_folds(DOBSCV_folds,DOBSCV_folds_y,file.split(".")[0]+"-DOBSCV",paht_output+"-DOBSCV/")





# CV = CrossValidation("originalDatasets/abalone_3_vs_11.arff",distance_func="default",file_type="arff")

# SCV_folds,SCV_folds_y,SCV_folds_inx=CV.SCV(foldNum=5)

# DBSCV_folds,DBSCV_folds_y,DBSCV_folds_inx=CV.DBSCV(foldNum=5)

# MSSCV_folds,MSSCV_folds_y,MSSCV_folds_inx=CV.MSSCV(foldNum=5)

# DOBSCV_folds,DOBSCV_folds_y,DOBSCV_folds_inx=CV.DOBSCV(foldNum=5)

# CV.write_folds(SCV_folds,SCV_folds_y,"abalone_3_vs_11-SCV","test_CV/")
# CV.write_folds(DBSCV_folds,DBSCV_folds_y,"abalone_3_vs_11-DBSCV","test_CV/")
# CV.write_folds(MSSCV_folds,MSSCV_folds_y,"abalone_3_vs_11-MSSCV","test_CV/")
# CV.write_folds(DOBSCV_folds,DOBSCV_folds_y,"abalone_3_vs_11-DOBSCV","test_CV/")