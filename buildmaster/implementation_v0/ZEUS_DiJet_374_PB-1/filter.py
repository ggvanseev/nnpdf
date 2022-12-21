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
    error_nuc = []

    for i in tables:
        if i == 12:
            q_sqr_min = 125
            q_sqr_max = 250
        elif i == 13:
            q_sqr_min = 250
            q_sqr_max = 500
        elif i == 14:
            q_sqr_min = 500
            q_sqr_max = 1000
        elif i == 15:
            q_sqr_min = 1000
            q_sqr_max = 2000
        elif i == 16:
            q_sqr_min = 2000
            q_sqr_max = 5000
        elif i == 17:
            q_sqr_min = 5000
            q_sqr_max = 1000
        q_sqr_central = None

        hepdata_tables="rawdata/Table"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = float(input['dependent_variables'][0]['qualifiers'][6]['value'])
        values_len = len(input['dependent_variables'][0]['values'])

        for j in range(values_len):
            data_central_value = input['dependent_variables'][0]['values'][j]['value']
            data_central.append(data_central_value)
            ET_max = input['independent_variables'][0]['values'][j]['high']
            ET_min = input['independent_variables'][0]['values'][j]['low']
            ET_central = None
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': q_sqr_central, 'max': q_sqr_max},'<ET>': {'min': ET_min, 'mid': ET_central, 'max': ET_max}}
            kin.append(kin_value)

    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

processData()