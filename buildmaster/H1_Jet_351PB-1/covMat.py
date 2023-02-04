import yaml
from numpy import array
from utils import corMat_to_covMat as ctc

corMatArray = array([100,-20,-11,-2,-14,2,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
-20,100,2,-1,4,-13,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
-11,2,100,6,1,0,-13,-1,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,
-2,-1,6,100,0,0,0,-14,0,0,0,2,0,0,0,0,0,0,0,1,0,0,0,1,
-14,4,1,0,100,-21,-10,-2,-11,2,1,0,-1,0,0,0,-1,0,0,0,0,0,0,0,
2,-13,0,0,-21,100,2,-1,3,-10,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,
1,0,-13,0,-10,2,100,7,1,1,-12,0,0,0,0,0,0,0,-1,0,0,0,0,0,
0,0,-1,-14,-2,-1,7,100,0,0,0,-11,0,0,0,0,0,0,0,-1,0,0,0,0,
1,0,0,0,-11,3,1,0,100,-23,-12,-2,-8,1,1,0,-1,0,0,0,0,0,0,0,
0,2,0,0,2,-10,1,0,-23,100,0,-2,2,-8,0,0,0,0,0,0,0,0,0,0,
0,0,2,0,1,0,-12,0,-12,0,100,5,1,1,-8,0,0,0,-1,0,0,0,0,0,
0,0,0,2,0,0,0,-11,-2,-2,5,100,0,0,0,-8,0,0,0,0,0,0,0,0,
0,0,0,0,-1,0,0,0,-8,2,1,0,100,-22,-11,-2,-4,1,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,-8,1,0,-22,100,-1,-2,1,-4,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,-8,0,-11,-1,100,5,0,1,-4,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,-8,-2,-2,5,100,0,0,0,-5,0,0,0,0,
0,0,0,0,-1,0,0,0,-1,0,0,0,-4,1,0,0,100,-24,-12,-2,-1,0,0,0,
0,0,0,0,0,-1,0,0,0,0,0,0,1,-4,1,0,-24,100,1,-2,0,-1,0,0,
0,0,0,0,0,0,-1,0,0,0,-1,0,0,0,-4,0,-12,1,100,3,0,0,-1,0,
0,0,0,1,0,0,0,-1,0,0,0,0,0,0,0,-5,-2,-2,3,100,0,0,0,-2,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,100,-21,-15,-3,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,-21,100,-1,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,-15,-1,100,-2,
0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-2,-3,0,-2,100])/100

with open('metadata.yaml', 'r') as file:
    metadata = yaml.safe_load(file)
tables = metadata['implemented_observables'][0]['tables']
tables_norm = metadata['implemented_observables'][1]['tables']
ndata = metadata['implemented_observables'][0]['ndata']
ndata_norm = metadata['implemented_observables'][1]['ndata']


hepdata_tables="rawdata/Table"+str(tables[0])+".yaml"
with open(hepdata_tables, 'r') as file:
    input = yaml.safe_load(file)

values = input['dependent_variables'][0]['values']
data_central = []
for i in range(len(values)):
    data_central_value = values[i]['value']
    data_central.append(data_central_value)
covMatArray = ctc(ndata, data_central, corMatArray)

hepdata_tables="rawdata/Table"+str(tables_norm[0])+".yaml"
with open(hepdata_tables, 'r') as file:
    input = yaml.safe_load(file)

values = input['dependent_variables'][0]['values']
data_central_norm = []
for i in range(len(values)):
    data_central_value = values[i]['value']
    data_central_norm.append(data_central_value)
covMatArray_norm = ctc(ndata_norm, data_central_norm, corMatArray)