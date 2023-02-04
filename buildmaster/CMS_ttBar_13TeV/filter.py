# implemented by Tanishq Sharma

import yaml
from utils import covMat_to_artSys as cta

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)

    tables_dSig_dmttBar = metadata['implemented_observables'][0]['tables']
    tables_dSig_dmttBar_norm = metadata['implemented_observables'][1]['tables']
    tables_dSig_dyttBar = metadata['implemented_observables'][2]['tables']
    tables_dSig_dyttBar_norm = metadata['implemented_observables'][3]['tables']
    tables_d2Sig_dyttbar_dmttbar = metadata['implemented_observables'][4]['tables']
    tables_d2Sig_dyttBar_dmttBar_norm = metadata['implemented_observables'][5]['tables']

    ndata_dSig_dmttBar = metadata['implemented_observables'][0]['ndata']
    ndata_dSig_dmttBar_norm = metadata['implemented_observables'][1]['ndata']
    ndata_dSig_dyttBar = metadata['implemented_observables'][2]['ndata']
    ndata_dSig_dyttBar_norm = metadata['implemented_observables'][3]['ndata']
    ndata_d2Sig_dyttbar_dmttbar = metadata['implemented_observables'][4]['ndata']
    ndata_d2Sig_dyttbar_dmttbar_norm = metadata['implemented_observables'][5]['ndata']

    data_central_dSig_dmttBar = []
    kin_dSig_dmttBar = []
    error_dSig_dmttBar = []
    data_central_dSig_dmttBar_norm = []
    kin_dSig_dmttBar_norm = []
    error_dSig_dmttBar_norm = []
    data_central_dSig_dyttBar = []
    kin_dSig_dyttBar = []
    error_dSig_dyttBar = []
    data_central_dSig_dyttBar_norm = []
    kin_dSig_dyttBar_norm = []
    error_dSig_dyttBar_norm = []
    data_central_d2Sig_dyttbar_dmttbar = []
    kin_d2Sig_dyttbar_dmttbar = []
    error_d2Sig_dyttbar_dmttbar = []
    data_central_d2Sig_dyttbar_dmttbar_norm = []
    kin_d2Sig_dyttbar_dmttbar_norm = []
    error_d2Sig_dyttbar_dmttbar_norm = []

    covMatArray_dSig_dmttBar = []
    covMatArray_dSig_dmttBar_norm = []
    covMatArray_dSig_dyttBar = []
    covMatArray_dSig_dyttBar_norm = []
    covMatArray_d2Sig_dyttbar_dmttbar = []
    covMatArray_d2Sig_dyttbar_dmttbar_norm = []

# dSig_dmttBar data

    hepdata_tables="rawdata/"+tables_dSig_dmttBar[0]+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    
    covariance_matrix="rawdata/parton_abs_ttm_covariance.yaml"
    with open(covariance_matrix, 'r') as file2:
        input2 = yaml.safe_load(file2)
    for i in range(ndata_dSig_dmttBar*ndata_dSig_dmttBar):
        covMatEl = input2['dependent_variables'][0]['values'][i]['value']
        covMatArray_dSig_dmttBar.append(covMatEl)
    artSysMat_dSig_dmttBar = cta(ndata_dSig_dmttBar, covMatArray_dSig_dmttBar)
    
    sqrt_s = 13000
    values = input['dependent_variables'][0]['values']
    
    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_dSig_dmttBar.append(data_central_value)
        m_ttBar_min = input['independent_variables'][0]['values'][i]['low']
        m_ttBar_max = input['independent_variables'][0]['values'][i]['high']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'm_ttBar': {'min': m_ttBar_min, 'mid': None, 'max': m_ttBar_max}}
        kin_dSig_dmttBar.append(kin_value)
        error_value = {}
        error_value['stat'] = values[i]['errors'][0]['symerror']
        error_value['sys'] = values[i]['errors'][1]['symerror']
        for j in range(ndata_dSig_dmttBar):
            error_value['ArtSys_'+str(j+1)] = 0 #artSysMat_dSig_dmttBar[][]
        error_dSig_dmttBar.append(error_value)
            
    error_definition_dSig_dmttBar = {}
    error_definition_dSig_dmttBar['stat'] = {'definition': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    error_definition_dSig_dmttBar['sys'] = {'definition': 'total systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    for i in range(ndata_dSig_dmttBar):
        error_definition_dSig_dmttBar['ArtSys_'+str(i+1)] = {'definition': 'artificial systematic uncertainty '+str(i+1), 'treatment': 'ADD', 'type': 'CORR'}
    data_central_dSig_dmttBar_yaml = {'data_central': data_central_dSig_dmttBar}
    kinematics_dSig_dmttBar_yaml = {'bins': kin_dSig_dmttBar}
    uncertainties_dSig_dmttBar_yaml = {'definitions': error_definition_dSig_dmttBar, 'bins': error_dSig_dmttBar}

    with open('data_dSig_dmttBar.yaml', 'w') as file:
         yaml.dump(data_central_dSig_dmttBar_yaml, file, sort_keys=False)

    with open('kinematics_dSig_dmttBar.yaml', 'w') as file:
         yaml.dump(kinematics_dSig_dmttBar_yaml, file, sort_keys=False)

    with open('uncertainties_dSig_dmttBar.yaml', 'w') as file:
        yaml.dump(uncertainties_dSig_dmttBar_yaml, file, sort_keys=False)

    
# dSig_dmttBar_norm data

    hepdata_tables="rawdata/"+tables_dSig_dmttBar_norm[0]+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)

    covariance_matrix="rawdata/parton_norm_ttm_covariance.yaml"
    with open(covariance_matrix, 'r') as file2:
        input2 = yaml.safe_load(file2)
    for i in range(ndata_dSig_dmttBar_norm*ndata_dSig_dmttBar_norm):
        covMatEl = input2['dependent_variables'][0]['values'][i]['value']
        covMatArray_dSig_dmttBar_norm.append(covMatEl)
    artSysMat_dSig_dmttBar_norm = cta(ndata_dSig_dmttBar_norm, covMatArray_dSig_dmttBar_norm)

    sqrt_s = 13000
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_dSig_dmttBar_norm.append(data_central_value)
        m_ttBar_min = input['independent_variables'][0]['values'][i]['low']
        m_ttBar_max = input['independent_variables'][0]['values'][i]['high']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'm_ttBar': {'min': m_ttBar_min, 'mid': None, 'max': m_ttBar_max}}
        kin_dSig_dmttBar_norm.append(kin_value)
        error_value = {}
        error_value['stat'] = values[i]['errors'][0]['symerror']
        error_value['sys'] = values[i]['errors'][1]['symerror']
        for j in range(ndata_dSig_dmttBar_norm):
            error_value['ArtSys_'+str(j+1)] = 0 #artSysMat_dSig_dmttBar_norm[][]
        error_dSig_dmttBar_norm.append(error_value)
    
    error_definition_dSig_dmttBar_norm = {}
    error_definition_dSig_dmttBar_norm['stat'] = {'definition': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    error_definition_dSig_dmttBar_norm['sys'] = {'definition': 'total systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    for i in range(ndata_dSig_dmttBar_norm):
        error_definition_dSig_dmttBar_norm['ArtSys_'+str(i+1)] = {'definition': 'artificial systematic uncertainty '+str(i+1), 'treatment': 'ADD', 'type': 'CORR'}

    data_central_dSig_dmttBar_norm_yaml = {'data_central': data_central_dSig_dmttBar_norm}
    kinematics_dSig_dmttBar_norm_yaml = {'bins': kin_dSig_dmttBar_norm}
    uncertainties_dSig_dmttBar_norm_yaml = {'definitions': error_definition_dSig_dmttBar_norm, 'bins': error_dSig_dmttBar_norm}

    with open('data_dSig_dmttBar_norm.yaml', 'w') as file:
         yaml.dump(data_central_dSig_dmttBar_norm_yaml, file, sort_keys=False)

    with open('kinematics_dSig_dmttBar_norm.yaml', 'w') as file:
         yaml.dump(kinematics_dSig_dmttBar_norm_yaml, file, sort_keys=False)

    with open('uncertainties_dSig_dmttBar_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_dSig_dmttBar_norm_yaml, file, sort_keys=False)

# dSig_dyttBar data

    hepdata_tables="rawdata/"+tables_dSig_dyttBar[0]+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    
    covariance_matrix="rawdata/parton_abs_tty_covariance.yaml"
    with open(covariance_matrix, 'r') as file2:
        input2 = yaml.safe_load(file2)
    for i in range(ndata_dSig_dyttBar*ndata_dSig_dyttBar):
        covMatEl = input2['dependent_variables'][0]['values'][i]['value']
        covMatArray_dSig_dyttBar.append(covMatEl)
    artSysMat_dSig_dyttBar = cta(ndata_dSig_dyttBar, covMatArray_dSig_dyttBar)

    sqrt_s = 13000
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_dSig_dyttBar.append(data_central_value)
        y_ttBar_min = input['independent_variables'][0]['values'][i]['low']
        y_ttBar_max = input['independent_variables'][0]['values'][i]['high']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'y_ttBar': {'min': y_ttBar_min, 'mid': None, 'max': y_ttBar_max}}
        kin_dSig_dyttBar.append(kin_value)
        error_value = {}
        error_value['stat'] = values[i]['errors'][0]['symerror']
        error_value['sys'] = values[i]['errors'][1]['symerror']
        for j in range(ndata_dSig_dyttBar):
            error_value['ArtSys_'+str(j+1)] = 0 #artSysMat_dSig_dyttBar[][]
        error_dSig_dyttBar.append(error_value)
    
    error_definition_dSig_dyttBar = {}
    error_definition_dSig_dyttBar['stat'] = {'definition': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    error_definition_dSig_dyttBar['sys'] = {'definition': 'total systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    for i in range(ndata_dSig_dyttBar):
        error_definition_dSig_dyttBar['ArtSys_'+str(i+1)] = {'definition': 'artificial systematic uncertainty '+str(i+1), 'treatment': 'ADD', 'type': 'CORR'}

    data_central_dSig_dyttBar_yaml = {'data_central': data_central_dSig_dyttBar}
    kinematics_dSig_dyttBar_yaml = {'bins': kin_dSig_dyttBar}
    uncertainties_dSig_dyttBar_yaml = {'definitions': error_definition_dSig_dyttBar, 'bins': error_dSig_dyttBar}

    with open('data_dSig_dyttBar.yaml', 'w') as file:
         yaml.dump(data_central_dSig_dyttBar_yaml, file, sort_keys=False)

    with open('kinematics_dSig_dyttBar.yaml', 'w') as file:
         yaml.dump(kinematics_dSig_dyttBar_yaml, file, sort_keys=False)

    with open('uncertainties_dSig_dyttBar.yaml', 'w') as file:
        yaml.dump(uncertainties_dSig_dyttBar_yaml, file, sort_keys=False)

# dSig_dyttBar_norm data

    hepdata_tables="rawdata/"+tables_dSig_dyttBar_norm[0]+".yaml"
    with open(hepdata_tables, 'r') as file:
        input = yaml.safe_load(file)
    
    covariance_matrix="rawdata/parton_norm_tty_covariance.yaml"
    with open(covariance_matrix, 'r') as file2:
        input2 = yaml.safe_load(file2)
    for i in range(ndata_dSig_dyttBar_norm*ndata_dSig_dyttBar_norm):
        covMatEl = input2['dependent_variables'][0]['values'][i]['value']
        covMatArray_dSig_dyttBar_norm.append(covMatEl)
    artSysMat_dSig_dyttBar_norm = cta(ndata_dSig_dyttBar_norm, covMatArray_dSig_dyttBar_norm)

    sqrt_s = 13000
    values = input['dependent_variables'][0]['values']

    for i in range(len(values)):
        data_central_value = values[i]['value']
        data_central_dSig_dyttBar_norm.append(data_central_value)
        y_ttBar_min = input['independent_variables'][0]['values'][i]['low']
        y_ttBar_max = input['independent_variables'][0]['values'][i]['high']
        kin_value = {'sqrt_s': {'min': None, 'mid': sqrt_s, 'max': None}, 'y_ttBar': {'min': y_ttBar_min, 'mid': None, 'max': y_ttBar_max}}
        kin_dSig_dyttBar_norm.append(kin_value)
        error_value = {}
        error_value['stat'] = values[i]['errors'][0]['symerror']
        error_value['sys'] = values[i]['errors'][1]['symerror']
        for j in range(ndata_dSig_dyttBar_norm):
            error_value['ArtSys_'+str(j+1)] = 0 #artSysMat_dSig_dyttBar_norm[][]
        error_dSig_dyttBar_norm.append(error_value)
    
    error_definition_dSig_dyttBar_norm = {}
    error_definition_dSig_dyttBar_norm['stat'] = {'definition': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    error_definition_dSig_dyttBar_norm['sys'] = {'definition': 'total systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    for i in range(ndata_dSig_dyttBar_norm):
        error_definition_dSig_dyttBar_norm['ArtSys_'+str(i+1)] = {'definition': 'artificial systematic uncertainty '+str(i+1), 'treatment': 'ADD', 'type': 'CORR'}

    data_central_dSig_dyttBar_norm_yaml = {'data_central': data_central_dSig_dyttBar_norm}
    kinematics_dSig_dyttBar_norm_yaml = {'bins': kin_dSig_dyttBar_norm}
    uncertainties_dSig_dyttBar_norm_yaml = {'definitions': error_definition_dSig_dyttBar_norm, 'bins': error_dSig_dyttBar_norm}

    with open('data_dSig_dyttBar_norm.yaml', 'w') as file:
         yaml.dump(data_central_dSig_dyttBar_norm_yaml, file, sort_keys=False)

    with open('kinematics_dSig_dyttBar_norm.yaml', 'w') as file:
         yaml.dump(kinematics_dSig_dyttBar_norm_yaml, file, sort_keys=False)

    with open('uncertainties_dSig_dyttBar_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_dSig_dyttBar_norm_yaml, file, sort_keys=False)

# d2Sig_dyttBar_dmttBar data

    covariance_matrix="rawdata/parton_abs_ttm+tty_covariance.yaml"
    with open(covariance_matrix, 'r') as file2:
        input2 = yaml.safe_load(file2)
    for i in range(ndata_d2Sig_dyttbar_dmttbar*ndata_d2Sig_dyttbar_dmttbar):
        covMatEl = input2['dependent_variables'][0]['values'][i]['value']
        covMatArray_d2Sig_dyttbar_dmttbar.append(covMatEl)
    artSysMat_d2Sig_dyttbar_dmttbar = cta(ndata_d2Sig_dyttbar_dmttbar, covMatArray_d2Sig_dyttbar_dmttbar)

    for i in tables_d2Sig_dyttbar_dmttbar:
        hepdata_tables="rawdata/parton_abs_ttm+tty_"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = 13000
        m_ttBar_min = input['dependent_variables'][0]['qualifiers'][0]['value']
        m_ttBar_max = input['dependent_variables'][0]['qualifiers'][1]['value']
        values = input ['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = values[j]['value']
            data_central_d2Sig_dyttbar_dmttbar.append(data_central_value)
            y_ttBar_min = input['independent_variables'][0]['values'][j]['low']
            y_ttBar_max = input['independent_variables'][0]['values'][j]['high']
            kin_value = {'sqrt_s':{'min': None,'mid': sqrt_s,'max': None}, 'm_ttBar':{'min': m_ttBar_min,'mid': None,'max': m_ttBar_max}, 'y_ttBar':{'min': y_ttBar_min,'mid': None,'max': y_ttBar_max}}
            kin_d2Sig_dyttbar_dmttbar.append(kin_value)
            error_value = {}
            error_value['stat'] = values[j]['errors'][0]['symerror']
            error_value['sys'] = values[j]['errors'][1]['symerror']
            for k in range(ndata_d2Sig_dyttbar_dmttbar):
                error_value['ArtSys_'+str(k+1)] = 0 #artSysMat_d2Sig_dyttbar_dmttbar[][]
            error_d2Sig_dyttbar_dmttbar.append(error_value)

    error_definition_d2Sig_dyttbar_dmttbar = {}
    error_definition_d2Sig_dyttbar_dmttbar['stat'] = {'definition': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    error_definition_d2Sig_dyttbar_dmttbar['sys'] = {'definition': 'total systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    for i in range(ndata_d2Sig_dyttbar_dmttbar):
        error_definition_d2Sig_dyttbar_dmttbar['ArtSys_'+str(i+1)] = {'definition': 'artificial systematic uncertainty '+str(i+1), 'treatment': 'ADD', 'type': 'CORR'}

    data_central_d2Sig_dyttbar_dmttbar_yaml = {'data_central': data_central_d2Sig_dyttbar_dmttbar}
    kinematics_d2Sig_dyttbar_dmttbar_yaml = {'bins': kin_d2Sig_dyttbar_dmttbar}
    uncertainties_d2Sig_dyttbar_dmttbar_yaml = {'definitions': error_definition_d2Sig_dyttbar_dmttbar, 'bins': error_d2Sig_dyttbar_dmttbar}

    with open('data_d2Sig_dyttbar_dmttbar.yaml', 'w') as file:
         yaml.dump(data_central_d2Sig_dyttbar_dmttbar_yaml, file, sort_keys=False)

    with open('kinematics_d2Sig_dyttbar_dmttbar.yaml', 'w') as file:
         yaml.dump(kinematics_d2Sig_dyttbar_dmttbar_yaml, file, sort_keys=False)

    with open('uncertainties_d2Sig_dyttbar_dmttbar.yaml', 'w') as file:
        yaml.dump(uncertainties_d2Sig_dyttbar_dmttbar_yaml, file, sort_keys=False)

# d2Sig_dyttBar_dmttBar_norm data

    covariance_matrix="rawdata/parton_norm_ttm+tty_covariance.yaml"
    with open(covariance_matrix, 'r') as file2:
        input2 = yaml.safe_load(file2)
    for i in range(ndata_d2Sig_dyttbar_dmttbar_norm*ndata_d2Sig_dyttbar_dmttbar_norm):
        covMatEl = input2['dependent_variables'][0]['values'][i]['value']
        covMatArray_d2Sig_dyttbar_dmttbar_norm.append(covMatEl)
    artSysMat_d2Sig_dyttbar_dmttbar_norm = cta(ndata_d2Sig_dyttbar_dmttbar_norm, covMatArray_d2Sig_dyttbar_dmttbar_norm)

    for i in tables_d2Sig_dyttBar_dmttBar_norm:
        hepdata_tables="rawdata/parton_norm_ttm+tty_"+str(i)+".yaml"
        with open(hepdata_tables, 'r') as file:
            input = yaml.safe_load(file)

        sqrt_s = 13000
        m_ttBar_min = input['dependent_variables'][0]['qualifiers'][0]['value']
        m_ttBar_max = input['dependent_variables'][0]['qualifiers'][1]['value']
        values = input ['dependent_variables'][0]['values']

        for j in range(len(values)):
            data_central_value = values[j]['value']
            data_central_d2Sig_dyttbar_dmttbar_norm.append(data_central_value)
            y_ttBar_min = input['independent_variables'][0]['values'][j]['low']
            y_ttBar_max = input['independent_variables'][0]['values'][j]['high']
            kin_value = {'sqrt_s':{'min': None,'mid': sqrt_s,'max': None}, 'm_ttBar':{'min': m_ttBar_min,'mid': None,'max': m_ttBar_max}, 'y_ttBar':{'min': y_ttBar_min,'mid': None,'max': y_ttBar_max}}
            kin_d2Sig_dyttbar_dmttbar_norm.append(kin_value)
            error_value = {}
            error_value['stat'] = values[j]['errors'][0]['symerror']
            error_value['sys'] = values[j]['errors'][1]['symerror']
            for k in range(ndata_d2Sig_dyttbar_dmttbar_norm):
                error_value['ArtSys_'+str(k+1)] = 0 #artSysMat_d2Sig_dyttbar_dmttbar_norm[][]
            error_d2Sig_dyttbar_dmttbar_norm.append(error_value)

    error_definition_d2Sig_dyttbar_dmttbar_norm = {}
    error_definition_d2Sig_dyttbar_dmttbar_norm['stat'] = {'definition': 'total statistical uncertainty', 'treatment': 'ADD', 'type': 'UNCORR'}
    error_definition_d2Sig_dyttbar_dmttbar_norm['sys'] = {'definition': 'total systematic uncertainty', 'treatment': 'MULT', 'type': 'CORR'}
    for i in range(ndata_d2Sig_dyttbar_dmttbar_norm):
        error_definition_d2Sig_dyttbar_dmttbar_norm['ArtSys_'+str(i+1)] = {'definition': 'artificial systematic uncertainty '+str(i+1), 'treatment': 'ADD', 'type': 'CORR'}

    data_central_d2Sig_dyttbar_dmttbar_norm_yaml = {'data_central': data_central_d2Sig_dyttbar_dmttbar_norm}
    kinematics_d2Sig_dyttbar_dmttbar_norm_yaml = {'bins': kin_d2Sig_dyttbar_dmttbar_norm}
    uncertainties_d2Sig_dyttbar_dmttbar_norm_yaml = {'definitions': error_definition_d2Sig_dyttbar_dmttbar_norm, 'bins': error_d2Sig_dyttbar_dmttbar_norm}

    with open('data_d2Sig_dyttbar_dmttbar_norm.yaml', 'w') as file:
         yaml.dump(data_central_d2Sig_dyttbar_dmttbar_norm_yaml, file, sort_keys=False)

    with open('kinematics_d2Sig_dyttbar_dmttbar_norm.yaml', 'w') as file:
         yaml.dump(kinematics_d2Sig_dyttbar_dmttbar_norm_yaml, file, sort_keys=False)

    with open('uncertainties_d2Sig_dyttbar_dmttbar_norm.yaml', 'w') as file:
        yaml.dump(uncertainties_d2Sig_dyttbar_dmttbar_norm_yaml, file, sort_keys=False)

processData()