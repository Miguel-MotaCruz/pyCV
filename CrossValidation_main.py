
from .CrossValidation import CrossValidation
import os
import json
import concurrent.futures
import functools

# origin_folder = "arff_datasets"
# origin_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/arff_datasets"
# origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/CAT-DATA-ECAI-2021"
# origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/MIX-DATA-ECAI-2021"
# origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/NUM-DATA-ECAI-2021"

# destination_folder = "/Users/miguel_cruz/Library/CloudStorage/OneDrive-UniversidadedeCoimbra/CV_Kfold/arff_datasets_folds_v2"
# destination_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/src/CV_algorithms/pyCV/new_partitions"
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


def process_file(file, partitioned_files, ARFF_folder, Partitions_folder ,reps, force_rewrite,max_lines, partitioned_files_json, save_partitions):
    if file.endswith(".arff"):
        if file not in partitioned_files[Partitions_folder] or force_rewrite:
            CV = CrossValidation(os.path.join(os.path.abspath(ARFF_folder),file),distance_func="default",file_type="arff")
            if(max_lines==-1 or len(CV.X) < max_lines):
                print(file)
                for i in range(1,reps+1):
                    try:
                        scv(file=file, i=i, CV=CV, save=save_partitions, destination_folder=Partitions_folder)
                        dbscv(file=file, i=i, CV=CV, save=save_partitions, destination_folder=Partitions_folder)
                        msscv(file=file, i=i, CV=CV, save=save_partitions, destination_folder=Partitions_folder)
                        dobscv(file=file, i=i, CV=CV, save=save_partitions, destination_folder=Partitions_folder)
                    except Exception as e:
                        print("An error occurred: ", e)


                partitioned_files[Partitions_folder].append(file)
                with open(partitioned_files_json, "w") as outfile:
                    json.dump(partitioned_files, outfile)


def main(ARFF_folder, Partitions_folder,partitioned_files_json ,reps=200, max_lines=-1 ,save_partitions=True, force_rewrite=False):
    # reps = 200
    # save = save_partitions
    partitioned_files_json = partitioned_files_json
    if not os.path.exists(partitioned_files_json):
        os.makedirs(partitioned_files_json)


    if os.path.exists(partitioned_files_json):
        if os.stat(partitioned_files_json).st_size != 0:  # Check if the file is not empty
            with open(partitioned_files_json) as json_file:
                partitioned_files = json.load(json_file)
        else:
            partitioned_files = {}
    else:
        partitioned_files = {}

    if Partitions_folder not in partitioned_files:
        partitioned_files[Partitions_folder] = []
        with open(partitioned_files_json, "w") as outfile:
            json.dump(partitioned_files, outfile)
    
    

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(functools.partial(process_file, partitioned_files=partitioned_files, ARFF_folder=ARFF_folder, Partitions_folder=Partitions_folder, reps=reps, force_rewrite=force_rewrite, max_lines=max_lines, partitioned_files_json=partitioned_files_json, save_partitions=save_partitions), os.listdir(ARFF_folder))
    # for file in os.listdir(origin_folder):
    #         if file.endswith(".arff"):
    #             if file not in partitioned_files[destination_folder]:
    #                 print(file)
    #                 CV = CrossValidation(os.path.join(os.path.abspath(origin_folder),file),distance_func="default",file_type="arff")
    #                 for i in range(1,reps+1):
    #                     scv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
    #                     dbscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
    #                     msscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)
    #                     dobscv(file=file, i=i, CV=CV, save=save, destination_folder=destination_folder)

    #                 partitioned_files[destination_folder].append(file)
    #                 with open("partitioned_files.json", "w") as outfile:
    #                     json.dump(partitioned_files, outfile)



def count_samples(max_lines=300, ARFF_folder="arff_datasets"):
    count = 0
    for file in os.listdir(ARFF_folder):
        if file.endswith(".arff"):
            #print the name of the dataset and the number of samples per dataset, the print should not end with a new line
            print(file.split("/")[-1], end="")

            CV = CrossValidation(os.path.join(os.path.abspath(ARFF_folder),file),distance_func="default",file_type="arff")
            accept = "\t\t√" if len(CV.X) < max_lines else "\t"
            if(len(CV.X) < max_lines): count+=1
            print(accept, " - " ,len(CV.X))
    print("Accept: ",count)

if __name__ == "__main__":
    main()
    # count_samples()