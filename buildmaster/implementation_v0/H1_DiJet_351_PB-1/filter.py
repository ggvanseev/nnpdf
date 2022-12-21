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

    hepdata_tables="rawdata/Table7.yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][4]['value'])
    values_len = len(input['dependent_variables'][0]['values'])

    for i in range(values_len):
        data_central_value = input['dependent_variables'][0]['values'][i]['value']
        data_central.append(data_central_value)
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        pT_max = input['independent_variables'][1]['values'][i]['high']
        pT_min = input['independent_variables'][1]['values'][i]['low']        
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'<pT>': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin.append(kin_value)

    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

processData()