import yaml


def get_kinematics(tables, version):
    """
    returns the relevant kinematics values. 

    Parameters
    ----------
    tables : list
            list that enumerates the table number

    version : int
            integer read from metadata.yaml that
            indicated the version of the hepdata
            tables

    Returns
    -------
    list
        list containing the kinematic values for all
        hepdata tables
    """
    kin = []

    for table in tables:
        hepdata_table = f"rawdata/HEPData-ins1768911-v{version}-Table_{table}.yaml"

        with open(hepdata_table, 'r') as file:
            input = yaml.safe_load(file)

        for pt in input["independent_variables"][0]['values']:

            kin_value = {
                'pt': {'min': pt['low'], 'mid': 0.5 * (pt['low'] + pt['high']), 'max': pt['high']},
                'sqrt_s': {'min': None, 'mid': 13000.0, 'max': None},
            }

            kin.append(kin_value)

    return kin


def get_data_values(tables, version):
    """
    returns the central data.

    Parameters
    ----------
    tables : list
            list that enumerates the table number

    version : int
            integer read from metadata.yaml that
            indicated the version of the hepdata
            tables

    Returns
    -------
    list
        list containing the central values for all
        hepdata tables

    """

    data_central = []
    for table in tables:
        hepdata_table = f"rawdata/HEPData-ins1768911-v{version}-Table_{table}.yaml"

        with open(hepdata_table, 'r') as file:
            input = yaml.safe_load(file)

        values = input['dependent_variables'][0]['values']
        
        for value in values:
            data_central.append(value['value'])

    return data_central



if __name__ == "__main__":
    get_kinematics(tables=[7],version=3)
    get_data_values(tables=[7], version=3)