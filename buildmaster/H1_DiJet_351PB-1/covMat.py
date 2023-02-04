import yaml
from numpy import array
from utils import corMat_to_covMat as ctc

corMatArray = array([100,-44,11,3,-3,6,-2,0,11,-1,0,0,9,0,0,0,8,0,0,0,2,0,0,0,
-44,100,-36,-9,7,-13,5,1,-1,2,-1,0,0,1,0,0,0,1,0,0,0,0,0,0,
11,-36,100,6,-1,4,-14,0,0,-1,2,0,0,0,1,0,0,0,1,0,0,0,1,0,
3,-9,6,100,0,1,0,-14,0,0,0,2,0,0,0,0,0,0,0,1,0,0,0,1,
-3,7,-1,0,100,-44,10,2,-4,6,-1,0,4,1,0,0,4,1,0,0,1,0,0,0,
6,-13,4,1,-44,100,-34,-8,7,-11,4,1,1,-1,0,0,2,-1,0,0,0,0,0,0,
-2,5,-14,0,10,-34,100,2,-1,4,-12,0,0,0,0,0,0,0,-1,0,0,0,-1,0,
0,1,0,-14,2,-8,2,100,0,1,1,-11,0,0,0,0,0,0,1,-2,0,1,1,0,
11,-1,0,0,-4,7,-1,0,100,-47,11,3,-3,5,-1,0,4,1,0,0,1,0,0,0,
-1,2,-1,0,6,-11,4,1,-47,100,-34,-10,5,-8,3,1,1,0,0,0,0,0,0,0,
0,-1,2,0,-1,4,-12,1,11,-34,100,2,-1,3,-8,0,0,0,-1,1,0,0,-1,0,
0,0,0,2,0,1,0,-11,3,-10,2,100,0,1,0,-9,0,0,0,-1,0,0,0,0,
9,0,0,0,4,1,0,0,-3,5,-1,0,100,-45,11,3,-1,3,0,0,1,0,0,0,
0,1,0,0,1,-1,0,0,5,-8,3,1,-45,100,-36,-11,3,-4,2,1,0,0,0,0,
0,0,1,0,0,0,0,0,-1,3,-8,0,11,-35,100,4,0,2,-5,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,1,0,-9,3,-11,4,100,0,0,1,-6,0,0,1,1,
8,0,0,0,4,2,0,0,4,1,0,0,-1,3,0,0,100,-46,10,2,1,1,0,0,
0,1,0,0,1,-1,0,0,1,0,0,0,3,-4,2,0,-46,100,-35,-8,1,-1,0,0,
0,0,1,0,0,0,-1,1,0,0,-1,0,0,2,-5,1,10,-35,100,-3,0,1,-1,-1,
0,0,0,1,0,0,0,-2,0,0,1,-1,0,1,0,-6,2,-8,-3,100,0,0,1,2,
2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1,0,0,100,-41,7,2,
0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,-1,1,0,-41,100,-36,-9,
0,0,1,0,0,0,-1,1,0,0,-1,0,0,0,0,1,0,0,-1,1,7,-36,100,-13,
0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,-1,2,2,-9,-13,100])/100

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