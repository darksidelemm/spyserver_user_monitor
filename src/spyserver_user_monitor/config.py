#
#   Spyserver User Monitor - Configuration File Reader
#
from ruamel.yaml import YAML


def read_config(filename):
    """ Read in a configuration YAML file """
    with open(filename, 'r') as config_file:
        yaml = YAML(typ='safe')
        return yaml.load(config_file)


if __name__ == "__main__":
    import sys
    print(read_config(sys.argv[1]))