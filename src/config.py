from configparser import ConfigParser

def load_config(path: str) -> tuple:
    """Loads the configuration fro the config file into memory
    
    Args:
        path (str): the path of the config file

    Returns:
        tuple: the configs
    """

    config = ConfigParser()
    config.optionxform = str
    config.read(path)

    return dict(config)



if __name__ == "__main__":
    print(load_config("config.cfg"))

else:
    config = load_config("./config.cfg")

    # turn the str values to tuples and integers
    for section in config:
        config[section] = dict(config[section])
        for key, value in config[section].items():
            config[section][key] = eval(value)

    WINDOW = config["WINDOW"]
    PHYSICS = config["PHYSICS"]
    ENTITIES = config["ENTITIES"]
    ANIMATIONS = config["ANIMATIONS"]
