from CrossValidation import CrossValidation



CV = CrossValidation("originalDatasets/iris0.arff",distance_func="default",file_type="arff")


folds,folds_y,folds_inx=CV.SCV(foldNum=5)
folds,folds_y,folds_inx=CV.DBSCV(foldNum=5)
folds,folds_y,folds_inx=CV.MSSCV(foldNum=5)
folds,folds_y,folds_inx=CV.DOBSCV(foldNum=5)



CV.write_folds(folds,folds_y,"iris0","test_CV/")