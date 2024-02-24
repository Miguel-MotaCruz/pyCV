import pandas as pd
import arff
import os
from io import StringIO

#TODO - take care of strings

def convert_dat_to_arff(dataset_file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    print(script_dir)
    dataset_folder = os.path.join(
        os.path.abspath(script_dir),
        "originalDatasets",
    )
    dataset_path = os.path.join(
        os.path.abspath(dataset_folder),
        dataset_file_name,
    )
    new_dataset_path = os.path.join(
        os.path.abspath(dataset_folder),
        dataset_file_name.split(".")[0] + ".arff",
    )


    with open(dataset_path, "r") as file:
        lines = file.readlines()

 

    relation = [line.strip() for line in lines if line.startswith("@relation")]
    attribute_lines = [line.strip() for line in lines if line.startswith("@attribute")]
    # attribute_names = [line.split()[1] for line in attribute_lines]

    meta = []
    attributes = []
    attribute_names = []
    for line in attribute_lines:
        parts = line.split(" ", 2)
        attribute_name = parts[1]
        attribute_type = parts[2]

        # If the attribute type is a nominal or integer type, convert it to a list of values
        if attribute_type.startswith("{"):
            #i cannot use this split!! for example, in @attribute Class {1, 2}... i have to keep {1, 2}, and what u gave me is {1}
            attribute_type = [value.strip() for value in attribute_type[1:-1].split(",")]
            meta.append(0)
            # attribute_type = attribute_type[1:-1].split(",")
        elif attribute_type.startswith("integer"):
            attribute_type = 'NUMERIC'
            meta.append(1)
        elif attribute_type.startswith("real"):
            attribute_type = 'NUMERIC'
            meta.append(0)

        attributes.append((attribute_name, attribute_type))
        attribute_names.append(attribute_name)


    data_lines = [line.strip() for line in lines if not line.startswith("@")]
    dataset = pd.read_csv(
        StringIO("\n".join(data_lines)), header=None, names=attribute_names
    )
    print(dataset.head())
    data = []
    for col in dataset.columns:
        data.append(dataset[col].tolist())
    
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
    convert_dat_to_arff("ionosphere.dat")

if __name__ == "__main__":
    main()