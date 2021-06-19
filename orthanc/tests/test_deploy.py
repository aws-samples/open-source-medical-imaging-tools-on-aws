import json
import os
from time import strftime, localtime

CONFIG_FILE = 'orthanc-config.json'

def config_file_name():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONFIG_FILE))

def read_config_file():
    # print(config_file)
    with open(config_file_name(), "r") as read_file:
        data = json.load(read_file)
    return data

def write_config_file(params_dict):
    '''Write a config file with the given Parameters section
    '''
    now_str = strftime('%y%m%d_%H%M%S', localtime())
    print(now_str)
    config = read_config_file()
    config['StackName'] = now_str
    params_list = [{'ParameterKey': key, 'ParameterValue': value} for (key, value) in sorted(params_dict.items())]
    config['Parameters'] = params_list
    outfile = os.path.abspath(os.path.join(os.path.dirname(__file__), f'orthanc-config-{now_str}.json'))
    with open(outfile, 'w') as write_file:
        write_file.write(json.dumps(config, indent=4, sort_keys=True))

def get_parameters():
    '''Return a dictionary of the Parameter array
    '''
    config = read_config_file()
    parameter_list = config['Parameters']
    parameter_dict = {item['ParameterKey']: item['ParameterValue'] for item in parameter_list}
    # print(parameter_dict)
    return parameter_dict

def get_parameter(key):
    parameters = get_parameters()
    assert key in parameters
    return parameters[key]

def set_parameter(key, value):
    '''Return dictionary of the Parameter array, setting 'key' item to 'value'
    '''
    parameters = get_parameters()
    parameters[key] = value
    return parameters

def test_namespace():
    # namespace = get_parameter('Namespace')
    # print(namespace)
    parameters_dict = set_parameter('Namespace', 'xxx')
    print(parameters_dict)
    write_config_file(parameters_dict)
    # config = read_config_file()
    # get_parameter(config, 'InstanceType')
    assert True

def test_container_on_ec2():
    assert True