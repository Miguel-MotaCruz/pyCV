from CrossValidation import CrossValidation
import os
import json
import concurrent.futures
import functools
save = True

# origin_folder = "arff_datasets"
# origin_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/arff_datasets"
# origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/CAT-DATA-ECAI-2021"
# origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/MIX-DATA-ECAI-2021"
origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/NUM-DATA-ECAI-2021"

# destination_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/arff_datasets_folds_v2"
destination_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/src/CV_algorithms/pyCV/new_partitions"
# destination_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/lixo"


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
            os.makedirs(paht_output+"-DOBSCV")
        CV.write_folds(DOBSCV_folds,DOBSCV_folds_y,file.split(".")[0]+"-DOBSCV-{}".format(i),paht_output+"-DOBSCV/")


def process_file(file, processed_files, reps):
    if file.endswith(".arff"):
        if file not in processed_files[destination_folder]:
            CV = CrossValidation(os.path.join(os.path.abspath(origin_folder),file),distance_func="default",file_type="arff")
            if(len(CV.X) < 300):
                print(file)
                for i in range(1,reps+1):
                    try:
                        scv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                        dbscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                        msscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                        dobscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
                    except Exception as e:
                        print("An error occurred: ", e)


                processed_files[destination_folder].append(file)
                with open("processed_files.json", "w") as outfile:
                    json.dump(processed_files, outfile)


def main():
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

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(functools.partial(process_file, processed_files=processed_files, reps=reps), os.listdir(origin_folder))
    # for file in os.listdir(origin_folder):
    #         if file.endswith(".arff"):
    #             if file not in processed_files[destination_folder]:
    #                 print(file)
    #                 CV = CrossValidation(os.path.join(os.path.abspath(origin_folder),file),distance_func="default",file_type="arff")
    #                 for i in range(1,reps+1):
    #                     scv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
    #                     dbscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
    #                     msscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
    #                     dobscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)

    #                 processed_files[destination_folder].append(file)
    #                 with open("processed_files.json", "w") as outfile:
    #                     json.dump(processed_files, outfile)



def count_samples():
    count = 0
    for file in os.listdir(origin_folder):
        if file.endswith(".arff"):
            #print the name of the dataset and the number of samples per dataset, the print should not end with a new line
            print(file.split("/")[-1], end="")

            CV = CrossValidation(os.path.join(os.path.abspath(origin_folder),file),distance_func="default",file_type="arff")
            accept = "\t\t√" if len(CV.X) < 300 else "\t"
            if(len(CV.X) < 300): count+=1
            print(accept, " - " ,len(CV.X))
    print("Accept: ",count)

if __name__ == "__main__":
    main()
    # count_samples()