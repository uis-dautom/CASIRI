"""
Developed by Felipe Rubio
"""

import json

def selector():
    """
    Select between local or cloud deployment and return a variable with the value
    """
    while True:
        print("Please select an option")
        print("Press 1 for local deployment")
        print("Press 2 for cloud deployment")
        sparkplug_config = int(input(""))

        if sparkplug_config == 1:
            print("You have selected option 1 [Local Deployment] \n")
            break
        elif sparkplug_config == 2:
            print("You have selected option 2 [Cloud Deployment] \n")
            break
        else:
            print("Invalid option. Please choose a valid option")
    return sparkplug_config

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
