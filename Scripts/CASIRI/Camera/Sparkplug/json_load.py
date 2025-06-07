"""
Developed by Felipe Rubio
"""

import json

def cargar_json(file_name):
    """
    Loads a JSON file and returns its contents as a dictionary.
    
     Args:
         file_name (str): Name of the JSON file to load.

     Returns:
         dict: Content of the JSON file as a dictionary.
    """
    try:
        with open(file_name, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_name} was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"The file {file_name} is not a valid JSON file.")
