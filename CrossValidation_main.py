from CrossValidation import CrossValidation



CV = CrossValidation("originalDatasets/abalone_3_vs_11.arff",distance_func="default",file_type="arff")




SCV_folds,SCV_folds_y,SCV_folds_inx=CV.SCV(foldNum=5)

DBSCV_folds,DBSCV_folds_y,DBSCV_folds_inx=CV.DBSCV(foldNum=5)

MSSCV_folds,MSSCV_folds_y,MSSCV_folds_inx=CV.MSSCV(foldNum=5)

DOBSCV_folds,DOBSCV_folds_y,DOBSCV_folds_inx=CV.DOBSCV(foldNum=5)






CV.write_folds(SCV_folds,SCV_folds_y,"abalone_3_vs_11-SCV","test_CV/")
CV.write_folds(DBSCV_folds,DBSCV_folds_y,"abalone_3_vs_11-DBSCV","test_CV/")
CV.write_folds(MSSCV_folds,MSSCV_folds_y,"abalone_3_vs_11-MSSCV","test_CV/")
CV.write_folds(DOBSCV_folds,DOBSCV_folds_y,"abalone_3_vs_11-DOBSCV","test_CV/")