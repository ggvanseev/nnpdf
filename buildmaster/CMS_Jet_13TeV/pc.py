import yaml
import numpy
import pandas as pd 

tables = [
    'y1_y1',
    'y1_y2',
    'y1_y3',
    'y1_y4',
    'y2_y1',
    'y2_y2',
    'y2_y3',
    'y2_y4',
    'y3_y1',
    'y3_y2',
    'y3_y3',
    'y3_y4',
    'y4_y1',
    'y4_y2',
    'y4_y3',
    'y4_y4'
]

#print('-------r04-------')

for i in tables:
#    print('')
#    print(i)
#    print('')
    with open('rawdata/ak7_correlations_'+str(i)+'.yaml', 'r') as file:
        table = yaml.safe_load(file)

    entries = []
    for j in range(256):
        entries.append(table['dependent_variables'][0]['values'][j]['value'])
    
    matr = numpy.zeros((16, 16))

    for k in range(256):
        a = k // 16
        b = k % 16
        matr[a][b] = entries[k]

    pd.DataFrame(matr).to_csv('r07_'+str(i)+'.csv', header=None, index=None)
