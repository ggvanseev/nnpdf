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
        if i == 9:
            q_sqr_min = 5.5
            q_sqr_max = 8
        elif i == 10:
            q_sqr_min = 8
            q_sqr_max = 11
        elif i == 11:
            q_sqr_min = 11
            q_sqr_max = 16
        elif i == 12:
            q_sqr_min = 16
            q_sqr_max = 22
        elif i == 13:
            q_sqr_min = 22
            q_sqr_max = 30
        elif i == 14:
            q_sqr_min = 30
            q_sqr_max = 42
        elif i == 15:
            q_sqr_min = 42
            q_sqr_max = 60
        elif i == 16:
            q_sqr_min = 60
            q_sqr_max = 80
        q_sqr_central = None

        hepdata_tables="rawdata/data"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
        values_len = len(input['dependent_variables'][0]['values'])

        for j in range(values_len):
            data_central_value = input['dependent_variables'][0]['values'][j]['value']
            data_central.append(data_central_value)
            pT_max = input['independent_variables'][0]['values'][j]['high']
            pT_min = input['independent_variables'][0]['values'][j]['low']
            pT_central = None
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': q_sqr_central, 'max': q_sqr_max},'<pT>': {'min': pT_min, 'mid': pT_central, 'max': pT_max}}
            kin.append(kin_value)

    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

processData()