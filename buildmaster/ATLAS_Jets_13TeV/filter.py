import yaml
from utils import symmetrize_errors as se

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)

    tables_jet = metadata['implemented_observables'][0]['tables']
    tables_jet_altcorr1 = metadata['implemented_observables'][1]['tables']
    tables_dijet = metadata['implemented_observables'][2]['tables']

    data_central_jet = []
    kin_jet = []
    error_jet = []
    data_central_jet_altcorr1 = []
    kin_jet_altcorr1 = []
    error_jet_altcorr1 = []
    data_central_dijet = []
    kin_dijet = []
    error_dijet = []

# jet data

    for i in tables_jet:
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
        y_central = None
        hepdata_tables="rawdata/atlas_inclusive_jet2015_r04_eta"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        values = input['dependent_variables'][0]['values']
        sqrt_s = input['dependent_variables'][0]['qualifiers'][1]['value']

        for j in range(len(values)):
            pT_min = input['independent_variables'][0]['values'][j]['low']
            pT_max = input['independent_variables'][0]['values'][j]['high']
            value_delta = 0
            error_value = {}
            for k in range(len(values[j]['errors'])):
                se_delta, se_sigma = se(values[j]['errors'][k]['asymerror']['plus'], values[j]['errors'][k]['asymerror']['minus'])
                value_delta = value_delta + se_delta
                error_label = str(values[j]['errors'][k]['label'])
                error_value[error_label] = se_sigma
            data_central_value = values[j]['value'] + value_delta
            data_central_jet.append(data_central_value)
            error_jet.append(error_value)
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'pT': {'min': pT_min, 'mid': None, 'max': pT_max}, 'y': {'min': y_min, 'mid': y_central, 'max': y_max}}
            kin_jet.append(kin_value)

    hepdata_tables="rawdata/atlas_inclusive_jet2015_r04_eta1.yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    error_definition_jet = {}
    error_definition_jet['stat'] = {'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    for i in range(1, len(input['dependent_variables'][0]['values'][0]['errors'])):
        error_name = input['dependent_variables'][0]['values'][0]['errors'][i]['label']
        error_definition_jet[error_name] = {'description': '', 'treatment': 'MULT', 'type': 'CORR'}

    data_central_jet_yaml = {'data_central': data_central_jet}
    kinematics_jet_yaml = {'bins': kin_jet}
    uncertainties_jet_yaml = {'definitions': error_definition_jet, 'bins': error_jet}

    with open('data_jet.yaml', 'w') as file:
         yaml.dump(data_central_jet_yaml, file, sort_keys=False)

    with open('kinematics_jet.yaml', 'w') as file:
         yaml.dump(kinematics_jet_yaml, file, sort_keys=False)

    with open('uncertainties_jet.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_yaml, file, sort_keys=False)

# jet altcorr1 data

    for i in tables_jet_altcorr1:
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
        y_central = None
        hepdata_tables="rawdata/atlas_inclusive_jet2015_r04_altcorr1_eta"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        values = input['dependent_variables'][0]['values']
        sqrt_s = input['dependent_variables'][0]['qualifiers'][1]['value']

        for j in range(len(values)):
            pT_min = input['independent_variables'][0]['values'][j]['low']
            pT_max = input['independent_variables'][0]['values'][j]['high']
            value_delta = 0
            error_value = {}
            for k in range(len(values[j]['errors'])):
                se_delta, se_sigma = se(values[j]['errors'][k]['asymerror']['plus'], values[j]['errors'][k]['asymerror']['minus'])
                value_delta = value_delta + se_delta
                error_label = str(values[j]['errors'][k]['label'])
                error_value[error_label] = se_sigma
            data_central_value = values[j]['value'] + value_delta
            data_central_jet_altcorr1.append(data_central_value)
            error_jet_altcorr1.append(error_value)
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'pT': {'min': pT_min, 'mid': None, 'max': pT_max}, 'y': {'min': y_min, 'mid': y_central, 'max': y_max}}
            kin_jet_altcorr1.append(kin_value)

    hepdata_tables="rawdata/atlas_inclusive_jet2015_r04_altcorr1_eta1.yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    error_definition_jet_altcorr1 = {}
    error_definition_jet_altcorr1['stat'] = {'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    for i in range(1, len(input['dependent_variables'][0]['values'][0]['errors'])):
        error_name = input['dependent_variables'][0]['values'][0]['errors'][i]['label']
        error_definition_jet_altcorr1[error_name] = {'description': '', 'treatment': 'MULT', 'type': 'CORR'}

    data_central_jet_altcorr1_yaml = {'data_central': data_central_jet_altcorr1}
    kinematics_jet_altcorr1_yaml = {'bins': kin_jet_altcorr1}
    uncertainties_jet_altcorr1_yaml = {'definitions': error_definition_jet_altcorr1, 'bins': error_jet_altcorr1}

    with open('data_jet_altcorr1.yaml', 'w') as file:
         yaml.dump(data_central_jet_altcorr1_yaml, file, sort_keys=False)

    with open('kinematics_jet_altcorr1.yaml', 'w') as file:
         yaml.dump(kinematics_jet_altcorr1_yaml, file, sort_keys=False)

    with open('uncertainties_jet_altcorr1.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_altcorr1_yaml, file, sort_keys=False)

# dijet data

    for i in tables_dijet:
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
        y_central = None
        hepdata_tables="rawdata/atlas_mjj_jet2015_r04_ystar"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        values = input['dependent_variables'][0]['values']
        sqrt_s = input['dependent_variables'][0]['qualifiers'][1]['value']

        for j in range(len(values)):
            pT_min = input['independent_variables'][0]['values'][j]['low']
            pT_max = input['independent_variables'][0]['values'][j]['high']
            value_delta = 0
            error_value = {}
            for k in range(len(values[j]['errors'])):
                se_delta, se_sigma = se(values[j]['errors'][k]['asymerror']['plus'], values[j]['errors'][k]['asymerror']['minus'])
                value_delta = value_delta + se_delta
                error_label = str(values[j]['errors'][k]['label'])
                error_value[error_label] = se_sigma
            data_central_value = values[j]['value'] + value_delta
            data_central_dijet.append(data_central_value)
            error_dijet.append(error_value)
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'pT': {'min': pT_min, 'mid': None, 'max': pT_max}, 'y': {'min': y_min, 'mid': y_central, 'max': y_max}}
            kin_dijet.append(kin_value)

    hepdata_tables="rawdata/atlas_mjj_jet2015_r04_ystar1.yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    error_definition_dijet = {}
    error_definition_dijet['stat'] = {'description': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    for i in range(1, len(input['dependent_variables'][0]['values'][0]['errors'])):
        error_name = input['dependent_variables'][0]['values'][0]['errors'][i]['label']
        error_definition_dijet[error_name] = {'description': '', 'treatment': 'MULT', 'type': 'CORR'}

    data_central_dijet_yaml = {'data_central': data_central_dijet}
    kinematics_dijet_yaml = {'bins': kin_dijet}
    uncertainties_dijet_yaml = {'definitions': error_definition_dijet, 'bins': error_dijet}

    with open('data_dijet.yaml', 'w') as file:
         yaml.dump(data_central_dijet_yaml, file, sort_keys=False)

    with open('kinematics_dijet.yaml', 'w') as file:
         yaml.dump(kinematics_dijet_yaml, file, sort_keys=False)

    with open('uncertainties_dijet.yaml', 'w') as file:
        yaml.dump(uncertainties_dijet_yaml, file, sort_keys=False)

processData()
