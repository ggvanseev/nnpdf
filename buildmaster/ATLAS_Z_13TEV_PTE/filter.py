import yaml

from filter_utils import get_kinematics, get_data_values, get_systematics

UNCORRELATED_SYS = ["Stat (Data)", "Stat (MC)", "Efficiencies (Uncorellated)"]

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

    with open("metadata.yaml", "r") as file:
        metadata = yaml.safe_load(file)

    version = metadata["hepdata"]["version"]
    tables = metadata["hepdata"]["tables"]

    systematics = get_systematics(tables, version)

    # error definition
    error_definition = {}
    for table in tables: 
        uncertainties = systematics[table]

        for unc in uncertainties:

            if unc[0]['name'] in UNCORRELATED_SYS:
                error_definition[unc[0]['name']] = {
                    "description": f"{unc[0]['name']} from HEPDATA",
                    "treatment": "ADD",
                    "type": "UNCORR",
                }

            else:
                error_definition[unc[0]['name']] = {
                    "description": f"{unc[0]['name']} from HEPDATA",
                    "treatment": "ADD",
                    "type": "CORR",
                }

    # TODO:
    # store error in dict
    # error = []

    
    
    import IPython
    IPython.embed()




if __name__ == "__main__":
    filter_ATLAS_Z_13TEV_PTE_data_kinetic()
    filter_ATLAS_Z_13TEV_PTE_uncertainties()
