import pandas as pd
import arff
import os
from io import StringIO



def convert_dat_to_arff(dataset_file_name, origin_folder, destination_folder=None):
    '''
    Convert a .dat file to a .arff file
    :param dataset_file_name: The name of the .dat file
    :param dataset_folder: The relative path to folder where the .dat file is located
    :return: None
    '''


    script_dir = os.path.dirname(os.path.realpath(__file__))
    dataset_origin_folder = os.path.join(
        os.path.abspath(script_dir),
        origin_folder,
    )
    dataset_path = os.path.join(
        os.path.abspath(dataset_origin_folder),
        dataset_file_name,
    )

    if destination_folder is None:
        destination_folder = origin_folder
    

    dataset_destination_folder = os.path.join(
        os.path.abspath(script_dir),
        destination_folder,
    )
    if not os.path.exists(dataset_destination_folder):
        os.makedirs(dataset_destination_folder)
    new_dataset_path = os.path.join(
        os.path.abspath(dataset_destination_folder),
        dataset_file_name.split(".")[0] + ".arff",
    )


    with open(dataset_path, "r") as file:
        lines = file.readlines()


    relation = [line.strip() for line in lines if line.startswith("@relation")]
    attribute_lines = [line.strip() for line in lines if line.startswith("@attribute")]


    # meta = []
    attributes = []
    attribute_names = []
    for line in attribute_lines:
        parts = line.split(" ", 2)
        attribute_name = parts[1]
        attribute_type = parts[2]


        if attribute_type.startswith("{"):
            attribute_type = [value.strip() for value in attribute_type[1:-1].split(",")]
            # attribute_type = attribute_type[1:-1].split(",")
        elif attribute_type.startswith("integer") or attribute_type.startswith("real"):
            attribute_type = 'NUMERIC'

        attributes.append((attribute_name, attribute_type))
        attribute_names.append(attribute_name)


    data_lines = [line.strip() for line in lines if not line.startswith("@")]
    dataset = pd.read_csv(
        StringIO("\n".join(data_lines)), header=None, names=attribute_names
    )

    data = []
    for col in dataset.columns:
        data.append(dataset[col].tolist())
        # remove the quotes and spaces from the strings
        if dataset[col].dtype == 'object':
            data[-1] = [s.strip().strip("'") for s in data[-1]]
        

    data = list(map(list, zip(*data)))

    arff_data = {
        "description": "",
        "relation": relation[0].split()[1],
        "attributes": attributes,
        "data": data,
    }

    with open(new_dataset_path, "w", encoding="utf8") as f:
        arff.dump(arff_data, f)


def main():
    for file in os.listdir("datasets"):
        if file.endswith(".dat"):
            print(file)
            convert_dat_to_arff(file, "datasets", "arff_datasets")
    # convert_dat_to_arff("ionosphere.dat", "datasets")

if __name__ == "__main__":
    main()