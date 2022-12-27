import yaml
from utils import percentage_to_absolute as pta
from utils import symmetrize_errors as se
from math import sqrt

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)

    tables_jet = metadata['implemented_observables'][0]['tables']
    tables_jet_norm = metadata['implemented_observables'][1]['tables']
    tables_jet_highQ2 = metadata['implemented_observables'][2]['tables']
    tables_jet_highQ2_norm = metadata['implemented_observables'][3]['tables']
    tables_dijet = metadata['implemented_observables'][4]['tables']
    tables_dijet_norm = metadata['implemented_observables'][5]['tables']

    data_central_jet = []
    kin_jet = []
    error_jet = []
    data_central_jet_norm = []
    kin_jet_norm = []
    error_jet_norm = []
    data_central_jet_highQ2 = []
    kin_jet_highQ2 = []
    error_jet_highQ2 = []
    data_central_jet_highQ2_norm = []
    kin_jet_highQ2_norm = []
    error_jet_highQ2_norm = []
    data_central_dijet = []
    kin_dijet = []
    error_dijet = []
    data_central_dijet_norm = []
    kin_dijet_norm = []
    error_dijet_norm = []


# jet data

    for i in tables_jet:
        if i == 1:
            q_sqr_min = 5.5
            q_sqr_max = 8
        elif i == 2:
            q_sqr_min = 8
            q_sqr_max = 11
        elif i == 3:
            q_sqr_min = 11
            q_sqr_max = 16
        elif i == 4:
            q_sqr_min = 16
            q_sqr_max = 22
        elif i == 5:
            q_sqr_min = 22
            q_sqr_max = 30
        elif i == 6:
            q_sqr_min = 30
            q_sqr_max = 42
        elif i == 7:
            q_sqr_min = 42
            q_sqr_max = 60
        elif i == 8:
            q_sqr_min = 60
            q_sqr_max = 80

        hepdata_tables="rawdata/data"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
        values = input['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = float(values[j]['value'])
            pT_max = input['independent_variables'][0]['values'][j]['high']
            pT_min = input['independent_variables'][0]['values'][j]['low']
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
            kin_jet.append(kin_value)
            value_delta = 0
            error_value = {}
            error_value
            for k in 0, 1, 5, 6, 7, 8, 9, 10, 11:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']] = pta(values[j]['errors'][k]['symerror'], data_central_value)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value))
                    value_delta = value_delta + se_delta
                    error_value[values[j]['errors'][k]['label']] = se_sigma
            for k in 2, 3, 4:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']+'_1'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                    error_value[values[j]['errors'][k]['label']+'_2'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value)/sqrt(2), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value)/sqrt(2))
                    value_delta = value_delta + se_delta + se_delta
                    error_value[values[j]['errors'][k]['label']+'_1'] = se_sigma
                    error_value[values[j]['errors'][k]['label']+'_2'] = se_sigma
            data_central_value = data_central_value + value_delta
            data_central_jet.append(data_central_value)
            error_jet.append(error_value)

    error_definition_jet = {
        'stat':{'description': 'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Uncorr':{'description': 'systematic uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_1':{'description': 'MC model uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_2':{'description': 'MC model uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ModelRW_1':{'description': 'reweighting uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'ModelRW_2':{'description': 'reweighting uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'JES_1':{'description': 'jet energy scale uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'JES_2':{'description': 'jet energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'RCES':{'description': 'remaining cluster energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElEn':{'description': 'electron energy uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElTh':{'description': 'electron theta uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'Lumi':{'description': 'luminosity', 'treatment': 'MULT', 'type': 'CORR'},
        'LArN':{'description': 'lar noise', 'treatment': 'MULT', 'type': 'CORR'},
        'StatMC':{'description': 'MC statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'RadErr':{'description': 'radiative uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    }

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

    for i in tables_jet_norm:
        if i == 1:
            q_sqr_min = 5.5
            q_sqr_max = 8
        elif i == 2:
            q_sqr_min = 8
            q_sqr_max = 11
        elif i == 3:
            q_sqr_min = 11
            q_sqr_max = 16
        elif i == 4:
            q_sqr_min = 16
            q_sqr_max = 22
        elif i == 5:
            q_sqr_min = 22
            q_sqr_max = 30
        elif i == 6:
            q_sqr_min = 30
            q_sqr_max = 42
        elif i == 7:
            q_sqr_min = 42
            q_sqr_max = 60
        elif i == 8:
            q_sqr_min = 60
            q_sqr_max = 80

        hepdata_tables="rawdata/data"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
        values = input['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = float(values[j]['value'])
            pT_max = input['independent_variables'][0]['values'][j]['high']
            pT_min = input['independent_variables'][0]['values'][j]['low']
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
            kin_jet_norm.append(kin_value)
            value_delta = 0
            error_value = {}
            for k in 0, 1, 5, 6, 7, 8, 9, 10, 11:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']] = pta(values[j]['errors'][k]['symerror'], data_central_value)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value))
                    value_delta = value_delta + se_delta
                    error_value[values[j]['errors'][k]['label']] = se_sigma
            for k in 2, 3, 4:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']+'_1'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                    error_value[values[j]['errors'][k]['label']+'_2'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value)/sqrt(2), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value)/sqrt(2))
                    value_delta = value_delta + se_delta + se_delta
                    error_value[values[j]['errors'][k]['label']+'_1'] = se_sigma
                    error_value[values[j]['errors'][k]['label']+'_2'] = se_sigma
            data_central_value = data_central_value + value_delta
            data_central_jet_norm.append(data_central_value)
            error_jet_norm.append(error_value)

    error_definition_jet_norm = {
        'stat':{'description': 'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Uncorr':{'description': 'systematic uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_1':{'description': 'MC model uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_2':{'description': 'MC model uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ModelRW_1':{'description': 'reweighting uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'ModelRW_2':{'description': 'reweighting uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'JES_1':{'description': 'jet energy scale uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'JES_2':{'description': 'jet energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'RCES':{'description': 'remaining cluster energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElEn':{'description': 'electron energy uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElTh':{'description': 'electron theta uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'Lumi':{'description': 'luminosity', 'treatment': 'MULT', 'type': 'CORR'},
        'LArN':{'description': 'lar noise', 'treatment': 'MULT', 'type': 'CORR'},
        'StatMC':{'description': 'MC statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'RadErr':{'description': 'radiative uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    }

    data_central_jet_norm_yaml = {'data_central': data_central_jet_norm}
    kinematics_jet_norm_yaml = {'bins': kin_jet_norm}
    uncertainties_jet_norm_yaml = {'definitions': error_definition_jet_norm, 'bins': error_jet_norm}

    with open('data_jet_norm.yaml', 'w') as file:
        yaml.dump(data_central_jet_norm_yaml, file, sort_keys=False)

    with open('kinematics_jet_norm.yaml', 'w') as file:
        yaml.dump(kinematics_jet_norm_yaml, file, sort_keys=False)

    with open('uncertainties_jet_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_norm_yaml, file, sort_keys=False)

# jet_highQ2 data

    hepdata_tables="rawdata/data51.yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    
    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
    pT_min = 5
    pT_max = 7
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = float(values[i]['value'])
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin_jet_highQ2.append(kin_value)
        value_delta = 0
        error_value = {}
        for k in 0, 3, 4, 5, 6, 7, 8:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']] = pta(values[j]['errors'][k]['symerror'], data_central_value)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value))
                    value_delta = value_delta + se_delta
                    error_value[values[j]['errors'][k]['label']] = se_sigma
        for k in 1, 2:
            if 'symerror' in values[j]['errors'][k]:
                error_value[values[j]['errors'][k]['label']+'_1'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                error_value[values[j]['errors'][k]['label']+'_2'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
            else:
                se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value)/sqrt(2), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value)/sqrt(2))
                value_delta = value_delta + se_delta + se_delta
                error_value[values[j]['errors'][k]['label']+'_1'] = se_sigma
                error_value[values[j]['errors'][k]['label']+'_2'] = se_sigma
        data_central_value = data_central_value + value_delta
        data_central_jet_highQ2.append(data_central_value)
        error_jet_highQ2.append(error_value)
    
    error_definition_jet_highQ2 = {
        'stat':{'description':'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR' },
        'Model_1':{'description':'MC model uncertainty', 'treatment': 'ADD', 'type': 'UNCORR' },
        'Model_2':{'description':'MC model uncertainty', 'treatment': 'MULT', 'type': 'CORR' },
        'JES_1':{'description':'jet energy scale uncertainty', 'treatment': 'ADD', 'type': 'UNCORR' },
        'JES_2':{'description':'jet energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR' },
        'RCES':{'description':'remaining cluster energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR' },
        '$E_{e^\prime}$':{'description':'electron energy', 'treatment': 'MULT', 'type': 'CORR' },
        '$\theta_{e^\prime}$':{'description':'electron theta', 'treatment': 'MULT', 'type': 'CORR' },
        'ID(e)':{'description': 'electron identification', 'treatment': 'MULT', 'type': 'CORR'},
        'LArNoise':{'description':'lar noice', 'treatment': 'MULT', 'type': 'CORR' },
        'Norm':{'description': 'normalization uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    }

    data_central_jet_highQ2_yaml = {'data_central': data_central_jet_highQ2}
    kinematics_jet_highQ2_yaml = {'bins': kin_jet_highQ2}
    uncertainties_jet_highQ2_yaml = {'definitions': error_definition_jet_highQ2, 'bins': error_jet_highQ2}


    with open('data_jet_highQ2.yaml', 'w') as file:
        yaml.dump(data_central_jet_highQ2_yaml, file, sort_keys=False)

    with open('kinematics_jet_highQ2.yaml', 'w') as file:
        yaml.dump(kinematics_jet_highQ2_yaml, file, sort_keys=False)

    with open('uncertainties_jet_highQ2.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_highQ2_yaml, file, sort_keys=False)

# jet_highQ2_norm data

    hepdata_tables="rawdata/data52.yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    
    sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
    pT_min = 5
    pT_max = 7
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = float(values[i]['value'])
        q_sqr_max = input['independent_variables'][0]['values'][i]['high']
        q_sqr_min = input['independent_variables'][0]['values'][i]['low']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
        kin_jet_highQ2_norm.append(kin_value)
        value_delta = 0
        error_value = {}
        for k in 0, 3, 4, 5, 6:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']] = pta(values[j]['errors'][k]['symerror'], data_central_value)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value))
                    value_delta = value_delta + se_delta
                    error_value[values[j]['errors'][k]['label']] = se_sigma
        for k in 1, 2:
            if 'symerror' in values[j]['errors'][k]:
                error_value[values[j]['errors'][k]['label']+'_1'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                error_value[values[j]['errors'][k]['label']+'_2'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
            else:
                se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value)/sqrt(2), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value)/sqrt(2))
                value_delta = value_delta + se_delta + se_delta
                error_value[values[j]['errors'][k]['label']+'_1'] = se_sigma
                error_value[values[j]['errors'][k]['label']+'_2'] = se_sigma
        data_central_value = data_central_value + value_delta
        data_central_jet_highQ2_norm.append(data_central_value)
        error_jet_highQ2_norm.append(error_value)
    
    error_definition_jet_highQ2_norm = {
        'stat':{'description':'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR' },
        'Model_1':{'description':'MC model uncertainty', 'treatment': 'ADD', 'type': 'UNCORR' },
        'Model_2':{'description':'MC model uncertainty', 'treatment': 'MULT', 'type': 'CORR' },
        'JES_1':{'description':'jet energy scale uncertainty', 'treatment': 'ADD', 'type': 'UNCORR' },
        'JES_2':{'description':'jet energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR' },
        'RCES':{'description':'remaining cluster energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR' },
        '$E_{e^\prime}$':{'description':'electron energy', 'treatment': 'MULT', 'type': 'CORR' },
        '$\theta_{e^\prime}$':{'description':'electron theta', 'treatment': 'MULT', 'type': 'CORR' },
        'LArNoise':{'description':'lar noice', 'treatment': 'MULT', 'type': 'CORR' }
    }

    data_central_jet_highQ2_norm_yaml = {'data_central': data_central_jet_highQ2_norm}
    kinematics_jet_highQ2_norm_yaml = {'bins': kin_jet_highQ2_norm}
    uncertainties_jet_highQ2_norm_yaml = {'definitions': error_definition_jet_highQ2_norm, 'bins': error_jet_highQ2_norm}


    with open('data_jet_highQ2_norm.yaml', 'w') as file:
        yaml.dump(data_central_jet_highQ2_norm_yaml, file, sort_keys=False)

    with open('kinematics_jet_highQ2_norm.yaml', 'w') as file:
        yaml.dump(kinematics_jet_highQ2_norm_yaml, file, sort_keys=False)

    with open('uncertainties_jet_highQ2_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_jet_highQ2_norm_yaml, file, sort_keys=False)

# dijet data

    for i in tables_dijet:
        if i == 1:
            q_sqr_min = 5.5
            q_sqr_max = 8
        elif i == 2:
            q_sqr_min = 8
            q_sqr_max = 11
        elif i == 3:
            q_sqr_min = 11
            q_sqr_max = 16
        elif i == 4:
            q_sqr_min = 16
            q_sqr_max = 22
        elif i == 5:
            q_sqr_min = 22
            q_sqr_max = 30
        elif i == 6:
            q_sqr_min = 30
            q_sqr_max = 42
        elif i == 7:
            q_sqr_min = 42
            q_sqr_max = 60
        elif i == 8:
            q_sqr_min = 60
            q_sqr_max = 80

        hepdata_tables="rawdata/data"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
        values = input['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = float(values[j]['value'])
            pT_max = input['independent_variables'][0]['values'][j]['high']
            pT_min = input['independent_variables'][0]['values'][j]['low']
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
            kin_dijet.append(kin_value)
            value_delta = 0
            error_value = {}
            for k in 0, 1, 5, 6, 7, 8, 9, 10, 11:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']] = pta(values[j]['errors'][k]['symerror'], data_central_value)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value))
                    value_delta = value_delta + se_delta
                    error_value[values[j]['errors'][k]['label']] = se_sigma
            for k in 2, 3, 4:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']+'_1'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                    error_value[values[j]['errors'][k]['label']+'_2'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value)/sqrt(2), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value)/sqrt(2))
                    value_delta = value_delta + se_delta + se_delta
                    error_value[values[j]['errors'][k]['label']+'_1'] = se_sigma
                    error_value[values[j]['errors'][k]['label']+'_2'] = se_sigma
            data_central_value = data_central_value + value_delta
            data_central_dijet.append(data_central_value)
            error_dijet.append(error_value)

    error_definition_dijet = {
        'stat':{'description': 'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Uncorr':{'description': 'systematic uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_1':{'description': 'MC model uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_2':{'description': 'MC model uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ModelRW_1':{'description': 'reweighting uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'ModelRW_2':{'description': 'reweighting uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'JES_1':{'description': 'jet energy scale uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'JES_2':{'description': 'jet energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'RCES':{'description': 'remaining cluster energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElEn':{'description': 'electron energy uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElTh':{'description': 'electron theta uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'Lumi':{'description': 'luminosity', 'treatment': 'MULT', 'type': 'CORR'},
        'LArN':{'description': 'lar noise', 'treatment': 'MULT', 'type': 'CORR'},
        'StatMC':{'description': 'MC statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'RadErr':{'description': 'radiative uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    }

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

    for i in tables_dijet_norm:
        if i == 1:
            q_sqr_min = 5.5
            q_sqr_max = 8
        elif i == 2:
            q_sqr_min = 8
            q_sqr_max = 11
        elif i == 3:
            q_sqr_min = 11
            q_sqr_max = 16
        elif i == 4:
            q_sqr_min = 16
            q_sqr_max = 22
        elif i == 5:
            q_sqr_min = 22
            q_sqr_max = 30
        elif i == 6:
            q_sqr_min = 30
            q_sqr_max = 42
        elif i == 7:
            q_sqr_min = 42
            q_sqr_max = 60
        elif i == 8:
            q_sqr_min = 60
            q_sqr_max = 80

        hepdata_tables="rawdata/data"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = float(input['dependent_variables'][0]['qualifiers'][2]['value'])
        values = input['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = float(values[j]['value'])
            pT_max = input['independent_variables'][0]['values'][j]['high']
            pT_min = input['independent_variables'][0]['values'][j]['low']
            kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'q_sqr': {'min': q_sqr_min, 'mid': None, 'max': q_sqr_max},'pT': {'min': pT_min, 'mid': None, 'max': pT_max}}
            kin_dijet_norm.append(kin_value)
            value_delta = 0
            error_value = {}
            for k in 0, 1, 5, 6, 7, 8, 9, 10, 11:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']] = pta(values[j]['errors'][k]['symerror'], data_central_value)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value))
                    value_delta = value_delta + se_delta
                    error_value[values[j]['errors'][k]['label']] = se_sigma
            for k in 2, 3, 4:
                if 'symerror' in values[j]['errors'][k]:
                    error_value[values[j]['errors'][k]['label']+'_1'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                    error_value[values[j]['errors'][k]['label']+'_2'] = pta(values[j]['errors'][k]['symerror'], data_central_value)/sqrt(2)
                else:
                    se_delta, se_sigma = se(pta(values[j]['errors'][k]['asymerror']['plus'], data_central_value)/sqrt(2), pta(values[j]['errors'][k]['asymerror']['minus'], data_central_value)/sqrt(2))
                    value_delta = value_delta + se_delta + se_delta
                    error_value[values[j]['errors'][k]['label']+'_1'] = se_sigma
                    error_value[values[j]['errors'][k]['label']+'_2'] = se_sigma
            data_central_value = data_central_value + value_delta
            data_central_dijet_norm.append(data_central_value)
            error_dijet_norm.append(error_value)

    error_definition_dijet_norm = {
        'stat':{'description': 'statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Uncorr':{'description': 'systematic uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_1':{'description': 'MC model uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'Model_2':{'description': 'MC model uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ModelRW_1':{'description': 'reweighting uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'ModelRW_2':{'description': 'reweighting uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'JES_1':{'description': 'jet energy scale uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'JES_2':{'description': 'jet energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'RCES':{'description': 'remaining cluster energy scale uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElEn':{'description': 'electron energy uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'ElTh':{'description': 'electron theta uncertainty', 'treatment': 'MULT', 'type': 'CORR'},
        'Lumi':{'description': 'luminosity', 'treatment': 'MULT', 'type': 'CORR'},
        'LArN':{'description': 'lar noise', 'treatment': 'MULT', 'type': 'CORR'},
        'StatMC':{'description': 'MC statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'},
        'RadErr':{'description': 'radiative uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    }

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