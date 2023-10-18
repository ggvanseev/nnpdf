import yaml

from filter_utils import get_kinematics, get_data_values


def filter_ATLAS_Z_13TEV_PTE_data_kinetic():
    """
    TODO
    """
    with open("metadata.yaml", "r") as file:
        metadata = yaml.safe_load(file)

    version = metadata["hepdata"]["version"]
    tables = metadata["hepdata"]["tables"]

    kin = get_kinematics(tables, version)
    central_values = get_data_values(tables, version)

    data_central_yaml = {"data_central": central_values}
    kinematics_yaml = {"bins": kin}

    # write central values and kinematics to yaml file
    with open("data.yaml", "w") as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open("kinematics.yaml", "w") as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)


def filter_ATLAS_Z_13TEV_PTE_uncertainties():
    """
    TODO
    """


if __name__ == "__main__":
    filter_ATLAS_Z_13TEV_PTE_data_kinetic()
