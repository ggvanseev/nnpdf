import yaml
import pandas
import numpy as np


def filter_HERA_CC_318GEV_EP_SIGMARED():
    # Filename
    filename = 'HERACOMBCCEP920.csv'

    # Read data from csv
    data = pandas.read_csv('rawdata/'+filename, dtype=float)

    # Write central dat file   
    data_central = []
    for i in range(len(data['Sigma'])):
        data_central.append(float(data['Sigma'][i]))
        
    data_central_yaml = {"data_central": data_central}

    with open("data.yaml", "w") as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    # Write kin file
    kin = []
    for i in range(len(data['Sigma'])):
        kin_value = {
            "x":  {"min": None, "mid": float(data['x'][i]), "max": None},
            "Q2": {"min": None, "mid": float(data['Q2'][i]), "max": None},
            "y":  {"min": None, "mid": float(data['y'][i]), "max": None},
        }
        kin.append(kin_value)
    
    kinematics_yaml = {"bins": kin}

    with open("kinematics.yaml", "w") as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

    # Write unc file
    error = []
    nCorSys = 162
    
    for i in range(len(data['Sigma'])):

        perc = float(data['Sigma'][i]) * 1e-2

        sys = {}
        for j in range(nCorSys):
            sys["sys"+str(j+1)] = float(data['sys'+str(j+1)][i]) * perc
            
        error_value = {
            "stat": float(data['stat'][i]) * perc,
            "uncor": float(data['uncor'][i]) * perc,
            "delta_rel": float(data['delta_rel'][i]) * perc,
            "delta_1": float(data['delta_1'][i]) * perc,
            "delta_2": float(data['delta_2'][i]) * perc,
            "delta_3": float(data['delta_3'][i]) * perc,
            "delta_4": float(data['delta_4'][i]) * perc,
            "delta_gp": float(data['delta_gp'][i]) * perc,
            "delta_had": float(data['delta_had'][i]) * perc,
        }

        error_value.update(sys)
        error.append(error_value)
        
    description = {}
    for j in range(nCorSys):
        description["syst"+str(j+1)] = {"description" : "systematic uncertainty "+str(j+1),
                                     "treatment" : "MULT",
                                     "type" : "CORR"}
        
    error_definition = {
        "stat": {
            "description": "total statistical uncertainty",
            "treatment": "ADD",
            "type": "UNCORR",
        },
        "uncor": {
            "description": "total uncorrelated systematic uncertainty",
            "treatment": "ADD",
            "type": "UNCORR",
        },
        "delta_rel": {
            "description": "correlated procedural uncertainty (alternative combination)",
            "treatment": "MULT",
            "type": "HC_delta_rel",
        },
        "delta_1": {
            "description": "correlated procedural uncertainty (very low Q2 data from HERA I)",
            "treatment": "MULT",
            "type": "HC_delta_1",
        },
        "delta_2": {
            "description": "correlated procedural uncertainty (low Q2 data from HERA II)",
            "treatment": "MULT",
            "type": "HC_delta_2",
        },
        "delta_3": {
            "description": "correlated procedural uncertainty (medium and high Q2, HERA I and II)",
            "treatment": "MULT",
            "type": "HC_delta_3",
        },  
        "delta_4": {
            "description": "correlated procedural uncertainty (normalisation issues from HERA I and II)",
            "treatment": "MULT",
            "type": "HC_delta_4",
        },
        "delta_gp": {
            "description": "correlated procedural uncertainty (photoproduction background)",
            "treatment": "MULT",
            "type": "HC_delta_gp",
        },  
        "delta_had": {
            "description": "correlated procedural uncertainty (hadronic energy scale)",
            "treatment": "MULT",
            "type": "HC_delta_had",
        }   
    }
    
    error_definition.update(description)
    
    uncertainties_yaml = {"definitions": error_definition, "bins": error}

    with open("uncertainties.yaml", "w") as file:
        yaml.dump(uncertainties_yaml, file, sort_keys=False)   

# Main
filter_HERA_CC_318GEV_EP_SIGMARED()
