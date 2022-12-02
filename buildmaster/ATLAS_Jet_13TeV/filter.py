import sys
import yaml

def processData():
    with open('metadata.yaml', 'r') as file:
        metadata = yaml.safe_load(file)
