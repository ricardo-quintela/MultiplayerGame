import yaml

def load_config(path: str) -> tuple:
    """Loads the configuration fro the config file into memory
    
    Args:
        path (str): the path of the config file

    Returns:
        tuple: the configs
    """

    with open(path, "r", encoding="utf-8") as config_file:
        config_data: dict = yaml.safe_load(config_file)

    return config_data



if __name__ == "__main__":
    print(load_config("config.yml"))

else:
    config = load_config("config.yml")

    LOGGING = config["logging"]
    WINDOW = config["window"]
    PHYSICS = config["physics"]
    INPUT = config["input"]
    ENTITIES = config["entities"]
    ENEMIES = config["enemies"]
    ANIMATIONS = config["animations"]
    MODELS = config["models"]
    MAPS = config["maps"]
    SPRITES = config["sprites"]
    DEBUG = config["debugging"]
