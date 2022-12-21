import sys
import yaml
from utils import symmetrize_errors as se

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)

    tables = metadata['implemented_observables'][0]['tables']

    data_central = []
    kin = []
    error = []

    for i in tables:

        hepdata_tables="rawdata/Table"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        for j in 0, 1:
            if i == 4:
                if j == 0:
                    q_sqr_min = 125
                    q_sqr_max = 250
                elif j == 1:
                    q_sqr_min = 250
                    q_sqr_max = 500
            elif i == 5:
                if j == 0:
                    q_sqr_min = 500
                    q_sqr_max = 1000
                elif j == 1:
                    q_sqr_min = 1000
                    q_sqr_max = 2000
            elif i == 6:
                if j == 0:
                    q_sqr_min = 2000
                    q_sqr_max = 5000
                if j == 1:
                    q_sqr_min = 5000
                    q_sqr_max = None

            sqrt_s = float(input['dependent_variables'][j]['qualifiers'][5]['value'])
            values = input['dependent_variables'][j]['values']

            for k in range(len(values)):
                data_central_value = values[k]['value']
                ET_max = input['independent_variables'][0]['values'][k]['high']
                ET_min = input['independent_variables'][0]['values'][k]['low']
                kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'ET': {'min': ET_min, 'mid': None, 'max': ET_max}}
                kin.append(kin_value)
                error_value = {}
                error_value['stat'] = values[k]['errors'][0]['symerror']
                sys_delta, error_value['sys'] = se(values[k]['errors'][1]['asymerror']['plus'], values[k]['errors'][1]['asymerror']['minus'])
                jet_es_delta, error_value['jet_es'] = se(values[k]['errors'][2]['asymerror']['plus'], values[k]['errors'][2]['asymerror']['minus'])
                data_central_value = data_central_value + sys_delta + jet_es_delta
                data_central.append(data_central_value)
                error.append(error_value)

    error_definition = {
        'stat': {'description': 'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'sys': {'description': 'systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'jet_es': {'description': 'jet energy scale uncertainty', 'treatment': '', 'type': ''}
    }

    data_central_yaml = {'data_central': data_central}
    kinematics_yaml = {'bins': kin}
    uncertainties_yaml = {'definitions': error_definition, 'bins': error}

    with open('data.yaml', 'w') as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    with open('kinematics.yaml', 'w') as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

    with open('uncertainties.yaml', 'w') as file:
        yaml.dump(uncertainties_yaml, file, sort_keys=False)

processData()


    