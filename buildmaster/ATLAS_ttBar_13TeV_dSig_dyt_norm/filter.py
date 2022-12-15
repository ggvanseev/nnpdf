import sys
import yaml

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)
    
    version = metadata['hepdata']['version']
    tables = metadata['hepdata']['tables']

    data_central = []
    kin = []
    error = []

    hepdata_tables="rawdata/Table"+str(tables[0])+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][0]['value'])
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central.append(data_central_value)
        y_t_min = input['independent_variables'][0]['values'][i]['low']
        y_t_max = input['independent_variables'][0]['values'][i]['high']
        y_t_central = None
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'y_t': {'min': y_t_min, 'mid': y_t_central, 'max': y_t_max}}
        kin.append(kin_value)

    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

processData()