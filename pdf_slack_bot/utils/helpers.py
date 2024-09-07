import yaml
from box import Box

__all__ = ["DotDict", "load_yaml_file"]


# helper functions and classes
class DotDict(dict):
    """
    dot.notation access to dictionary attributes
    """
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def load_yaml_file(file_name):
    """
    function to load yaml file to Box object
    """
    return Box.from_yaml(filename=file_name, Loader=yaml.FullLoader)
