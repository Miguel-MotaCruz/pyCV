from CrossValidation import CrossValidation
import os
import json

save = True

# origin_folder = "arff_datasets"
origin_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/arff_datasets"
destination_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/arff_datasets_folds_v2"
# destination_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/src/CV_algorithms/pyCV/test_CV"
# destination_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/lixo"
reps = 200
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

#i have to load the processed files
if os.path.exists("processed_files.json"):
    with open("processed_files.json") as json_file:
        processed_files = json.load(json_file)
else:
    processed_files = {}

if destination_folder not in processed_files:
    processed_files[destination_folder] = []

foldNum = 5



def scv( file, i, CV, save, destination_folder):
    SCV_folds,SCV_folds_y,SCV_folds_inx=CV.SCV(foldNum=foldNum)
    if save:
        paht_output = os.path.join(os.path.abspath(destination_folder),file.split(".")[0])
        if not os.path.exists(paht_output+"-SCV"):
            os.makedirs(paht_output+"-SCV")
        CV.write_folds(SCV_folds,SCV_folds_y,file.split(".")[0]+"-SCV-{}".format(i),paht_output+"-SCV/")

def dbscv( file, i, CV, save, destination_folder):
    DBSCV_folds,DBSCV_folds_y,DBSCV_folds_inx=CV.DBSCV(foldNum=foldNum)
    if save:
        paht_output = os.path.join(os.path.abspath(destination_folder),file.split(".")[0])
        if not os.path.exists(paht_output+"-DBSCV"):
            os.makedirs(paht_output+"-DBSCV")
        CV.write_folds(DBSCV_folds,DBSCV_folds_y,file.split(".")[0]+"-DBSCV-{}".format(i),paht_output+"-DBSCV/")

def msscv( file, i, CV, save, destination_folder):
    MSSCV_folds,MSSCV_folds_y,MSSCV_folds_inx=CV.MSSCV(foldNum=foldNum)
    if save:
        paht_output = os.path.join(os.path.abspath(destination_folder),file.split(".")[0])
        if not os.path.exists(paht_output+"-MSSCV"):
            os.makedirs(paht_output+"-MSSCV")
        CV.write_folds(MSSCV_folds,MSSCV_folds_y,file.split(".")[0]+"-MSSCV-{}".format(i),paht_output+"-MSSCV/")

def dobscv( file, i, CV, save, destination_folder):
    DOBSCV_folds,DOBSCV_folds_y,DOBSCV_folds_inx=CV.DOBSCV(foldNum=foldNum)
    if save:
        paht_output = os.path.join(os.path.abspath(destination_folder),file.split(".")[0])
        if not os.path.exists(paht_output+"-DOBSCV"):
            os.makedidrs(paht_output+"-DOBSCV")
        CV.write_folds(DOBSCV_folds,DOBSCV_folds_y,file.split(".")[0]+"-DOBSCV-{}".format(i),paht_output+"-DOBSCV/")

for file in os.listdir(origin_folder):
        if file.endswith(".arff"):
            if file not in processed_files[destination_folder]:
                print(file)
                CV = CrossValidation(os.path.join(os.path.abspath(origin_folder),file),distance_func="default",file_type="arff")
                for i in range(1,reps+1):
                    scv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                    dbscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                    msscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                    dobscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)

                processed_files[destination_folder].append(file)
                with open("processed_files.json", "w") as outfile:
                    json.dump(processed_files, outfile)