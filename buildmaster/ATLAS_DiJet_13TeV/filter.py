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
        if i == 1:
            y_min = 0
            y_max = 0.5
        elif i == 2:
            y_min = 0.5
            y_max = 1
        elif i == 3:
            y_min = 1
            y_max = 1.5
        elif i == 4:
            y_min = 1.5
            y_max = 2
        elif i == 5:
            y_min = 2
            y_max = 2.5
        elif i == 6:
            y_min = 2.5
            y_max = 3
        y_central = float((y_min+y_max)/2)
        hepdata_tables="rawdata/atlas_mjj_jet2015_r04_ystar"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        values = input['dependent_variables'][0]['values']
        sqrt_s = input['dependent_variables'][0]['qualifiers'][1]['value']

        for j in range(len(values)):
            data_central_value = input['dependent_variables'][0]['values'][j]['value']
            data_central.append(data_central_value)
            m_jj_min = input['independent_variables'][0]['values'][j]['low']
            m_jj_max = input['independent_variables'][0]['values'][j]['high']
            m_jj_central = float((m_jj_min+m_jj_max)/2)
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'm_jj': {'min': m_jj_min, 'mid': m_jj_central, 'max': m_jj_max}, 'y*': {'min': y_min, 'mid': y_central, 'max': y_max}}
            kin.append(kin_value)
            
    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

processData()