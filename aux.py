import shutil
import os

def copy_files(file_dict, dest_dir):
    for src_dir, files in file_dict.items():
        for file in files:
            src_file = os.path.join(src_dir, file)
            if os.path.exists(src_file):
                shutil.copy(src_file, dest_dir)
            else:
                print(f"File {src_file} does not exist")

def get_existing_files(folder_path, file_list):
    existing_files = [file for file in file_list if os.path.exists(os.path.join(folder_path, file))]
    return existing_files


origin_folder = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/DATASETS/CAT-DATA-ECAI-2021"
partitioned_files = {origin_folder: ["caesarian-cat.arff", "hepatitis-cat.arff", "immunotherapy-cat.arff", "broadway2-cat.arff", "schizo-cat.arff", "student-g-cat.arff", "veteran-cat.arff", "traffic-cat.arff", "lymphography-v1-cat.arff", "cryotherapy-cat.arff", "servo-cat.arff", "fertility-diagnosis-cat.arff", "pharynx-1year-cat.arff", "creditscore-cat.arff", "lymphography-normal-fibrosis-cat.arff", "student-cg-cat.arff", "kidney-cat.arff", "broadwaymult0-cat.arff", "Edu-Data-HvsL-cat.arff", "pbc-cat.arff", "student-p-cat.arff", "icu-cat.arff", "cyyoung-cat.arff", "pharynx-3year-cat.arff", "heart-statlog-cat.arff", "cleveland-cat.arff", "pharynx-status-cat.arff", "broadwaymult3-cat.arff", "caesarian.arff", "cryotherapy.arff", "hepatitis.arff", "immunotherapy.arff", "creditscore.arff", "broadway3.arff", "broadway2.arff", "fertility-diagnosis.arff", "schizo.arff", "student-g.arff", "traffic.arff", "veteran.arff", "lymphography-v1.arff", "student-p.arff", "kidney.arff", "servo.arff", "lymphography-normal-fibrosis.arff", "pharynx-1year.arff", "cyyoung.arff", "pharynx-status.arff", "pharynx-3year.arff", "icu.arff", "heart-statlog.arff", "Edu-Data-HvsL.arff", "broadwaymult0.arff", "pbc.arff", "cleveland.arff", "broadwaymult6.arff", "broadwaymult4.arff", "broadwaymult3.arff", "broadwaymult5.arff", "glioma16.arff", "solvent.arff", "colon32.arff", "lupus.arff", "leukemia.arff", "appendicitis.arff", "bc-coimbra.arff", "breast-car.arff", "wine-1vs2.arff", "somerville.arff", "iris0.arff", "relax.arff", "parkinson.arff", "sonar.arff", "glass1.arff", "wpbc.arff", "ecoli_0_vs_1.arff", "newthyroid1.arff", "prnn_synth.arff", "hepato-PHvsALD.arff", "spectf.arff", "poker_9_vs_7.arff", "ecoli-0-1-3-7_vs_2-6.arff"]}
dest_dir = "/Users/miguel_cruz/Documents/Miguel_Cruz/LEI/CISUC/CrossValidation/src/DataCentre/Original_Datasets"
# copy_files(partitioned_files, dest_dir)

print(get_existing_files(origin_folder, partitioned_files[origin_folder]))



