import sys
import yaml
from utils import percentage_to_absolute as pta

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)

    tables_jet = metadata['implemented_observables'][0]['tables']
    tables_jet_norm = metadata['implemented_observables'][1]['tables']
    tables_dijet = metadata['implemented_observables'][2]['tables']
    tables_dijet_norm = metadata['implemented_observables'][3]['tables']

    data_central_jet = []
    kin_jet = []
    error_jet = []
    data_central_jet_norm = []
    kin_jet_norm = []
    error_jet_norm = []
    data_central_dijet = []
    kin_dijet = []
    error_dijet = []
    data_central_dijet_norm = []
    kin_dijet_norm = []
    error_dijet_norm = []

# jet data

    hepdata_tables="rawdata/Table"+str(tables_jet[0])+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][3]['value'])
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_jet.append(data_central_value)
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        pT_max = input['independent_variables'][1]['values'][i]['high']
        pT_min = input['independent_variables'][1]['values'][i]['low']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin_jet.append(kin_value)
        error_value = {}
        error_value['stat'] = pta(values[i]['errors'][0]['symerror'], data_central_value)
        error_value['sys'] = pta(values[i]['errors'][1]['symerror'], data_central_value)
        error_jet.append(error_value)

    error_definition_jet = {'stat':{'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}, 'sys':{'description': 'total systematic uncertainty', 'treatment':'MULT' , 'type': 'CORR'}}

    data_central_jet_yaml = {'data_central': data_central_jet}
    kinematics_jet_yaml = {'bins': kin_jet}
    uncertainties_jet_yaml = {'definitions': error_definition_jet, 'bins': error_jet}

    with open('data_jet.yaml', 'w') as file:
         yaml.dump(data_central_jet_yaml, file, sort_keys=False)

    with open('kinematics_jet.yaml', 'w') as file:
         yaml.dump(kinematics_jet_yaml, file, sort_keys=False)

    with open('uncertainties_jet.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_yaml, file, sort_keys=False)

 # jet_norm data

    hepdata_tables="rawdata/Table"+str(tables_jet_norm[0])+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][3]['value'])
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_jet_norm.append(data_central_value)
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        pT_max = input['independent_variables'][1]['values'][i]['high']
        pT_min = input['independent_variables'][1]['values'][i]['low']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin_jet_norm.append(kin_value)
        error_value = {}
        error_value['stat'] = pta(values[i]['errors'][0]['symerror'], data_central_value)
        error_value['sys'] = pta(values[i]['errors'][1]['symerror'], data_central_value)
        error_jet_norm.append(error_value)

    error_definition_jet_norm = {'stat':{'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}, 'sys':{'description': 'total systematic uncertainty', 'treatment':'MULT' , 'type': 'CORR'}}

    data_central_jet_norm_yaml = {'data_central': data_central_jet_norm}
    kinematics_jet_norm_yaml = {'bins': kin_jet_norm}
    uncertainties_jet_norm_yaml = {'definitions': error_definition_jet_norm, 'bins': error_jet_norm}

    with open('data_jet_norm.yaml', 'w') as file:
         yaml.dump(data_central_jet_norm_yaml, file, sort_keys=False)

    with open('kinematics_jet_norm.yaml', 'w') as file:
         yaml.dump(kinematics_jet_norm_yaml, file, sort_keys=False)

    with open('uncertainties_jet_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_norm_yaml, file, sort_keys=False)

# dijet data

    hepdata_tables="rawdata/Table"+str(tables_dijet[0])+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][4]['value'])
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_dijet.append(data_central_value)
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        pT_max = input['independent_variables'][1]['values'][i]['high']
        pT_min = input['independent_variables'][1]['values'][i]['low']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin_dijet.append(kin_value)
        error_value = {}
        error_value['stat'] = pta(values[i]['errors'][0]['symerror'], data_central_value)
        error_value['sys'] = pta(values[i]['errors'][1]['symerror'], data_central_value)
        error_dijet.append(error_value)

    error_definition_dijet = {'stat':{'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}, 'sys':{'description': 'total systematic uncertainty', 'treatment':'MULT' , 'type': 'CORR'}}

    data_central_dijet_yaml = {'data_central': data_central_dijet}
    kinematics_dijet_yaml = {'bins': kin_dijet}
    uncertainties_dijet_yaml = {'definitions': error_definition_dijet, 'bins': error_dijet}

    with open('data_dijet.yaml', 'w') as file:
         yaml.dump(data_central_dijet_yaml, file, sort_keys=False)

    with open('kinematics_dijet.yaml', 'w') as file:
         yaml.dump(kinematics_dijet_yaml, file, sort_keys=False)

    with open('uncertainties_dijet.yaml', 'w') as file:
        yaml.dump(uncertainties_dijet_yaml, file, sort_keys=False)

# dijet_norm data

    hepdata_tables="rawdata/Table"+str(tables_dijet_norm[0])+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][4]['value'])
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_dijet_norm.append(data_central_value)
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        pT_max = input['independent_variables'][1]['values'][i]['high']
        pT_min = input['independent_variables'][1]['values'][i]['low']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin_dijet_norm.append(kin_value)
        error_value = {}
        error_value['stat'] = pta(values[i]['errors'][0]['symerror'], data_central_value)
        error_value['sys'] = pta(values[i]['errors'][1]['symerror'], data_central_value)
        error_dijet_norm.append(error_value)

    error_definition_dijet_norm = {'stat':{'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}, 'sys':{'description': 'total systematic uncertainty', 'treatment':'MULT' , 'type': 'CORR'}}

    data_central_dijet_norm_yaml = {'data_central': data_central_dijet_norm}
    kinematics_dijet_norm_yaml = {'bins': kin_dijet_norm}
    uncertainties_dijet_norm_yaml = {'definitions': error_definition_dijet_norm, 'bins': error_dijet_norm}

    with open('data_dijet_norm.yaml', 'w') as file:
         yaml.dump(data_central_dijet_norm_yaml, file, sort_keys=False)

    with open('kinematics_dijet_norm.yaml', 'w') as file:
         yaml.dump(kinematics_dijet_norm_yaml, file, sort_keys=False)

    with open('uncertainties_dijet_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_dijet_norm_yaml, file, sort_keys=False)

processData()