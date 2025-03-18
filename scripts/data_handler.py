"""
This module is used to handle data in json format.
"""
import json
from dataclasses import dataclass

def load_data(filepath: str = 'configs.json') -> dict[str, str]:
    """
    Load data from a json file.
    
    Parameters
    ----------
    filepath : str, optional
        The path of the json file, by default 'configs.json'.

    Returns
    -------
    dict[str, str]
        The data in the json file.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return {}

def save_data(data: dict[str, str] | list[dict], filepath: str = 'configs.json'):
    """"
    Save data to a json file.
    
    Parameters
    ----------
    data : dict[str, str] | list[dict]
        The data to be saved.
    filepath : str, optional
        The path of the json file, by default 'configs.json'.

    Raises
    ------
    TypeError
        If the data type mismatch.
    """
    current_data = load_data(filepath)

    if isinstance(current_data, dict) and isinstance(data, dict):
        current_data.update(data)
    elif isinstance(current_data, list) and isinstance(data, list):
        current_data.extend(data)
    else:
        raise TypeError(f"Data type mismatch. {type(current_data)} != {type(data)}")

    with open(filepath, 'w') as f:
        json.dump(current_data, f, indent=4, ensure_ascii=False)

@dataclass
class Config:
    """
    A class to handle user configurations.
    
    Attributes
    ----------
    name : str
        The name of the configuration module.
    value : dict[str, str], optional
        The value of the configuration, by default None.
    flag : bool, optional
        A flag to indicate whether to load the value from file, by default True.
    path : str, optional
        The path of the json file, by default 'configs.json'.

    Methods
    -------
    save()
        Save the configuration to the json file.
    """
    name: str
    value: dict[str, str] = None
    flag: bool = True
    path: str = 'configs.json'

    def __post_init__(self):
        if not self.value and self.flag:
            self.value =load_data(self.path)[self.name]
            self.flag = False
    
    def save(self):
        save_data({self.name: self.value}, self.path)
