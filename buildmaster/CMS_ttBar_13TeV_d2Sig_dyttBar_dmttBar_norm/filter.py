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

    for i in tables:
        hepdata_tables="rawdata/parton_norm_ttm+tty_"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = 13000
        m_ttBar_min = input['dependent_variables'][0]['qualifiers'][0]['value']
        m_ttBar_max = input['dependent_variables'][0]['qualifiers'][1]['value']
        values = input ['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = values[j]['value']
            data_central.append(data_central_value)
            y_ttBar_min = input['independent_variables'][0]['values'][j]['low']
            y_ttBar_max = input['independent_variables'][0]['values'][j]['high']
            kin_value = {'sqrt_s':{'min': None,'mid': sqrt_s,'max': None}, 'm_ttBar':{'min': m_ttBar_min,'mid': None,'max': m_ttBar_max}, 'y_ttBar':{'min': y_ttBar_min,'mid': None,'max': y_ttBar_max}}
            kin.append(kin_value)

    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

processData()