import configobj


def get_config(config_filepath):
    config = configobj.ConfigObj(config_filepath)

    return config
