from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import pickle

from bgpy.simulation_engine import ASRA
from bgpy.simulation_framework import GraphFactory, LineInfo

BASE_PATH = Path("/home/anon/aspa_sims_2024_10_14_raw")

# Custom Unpickler class to handle missing modules/classes
class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Check if the missing class is from the 'bgpy.simulation_engine.policies.aspa.aspawn' module
        if module == 'bgpy.simulation_engine.policies.aspa.aspawn':
            print(f"Module '{module}' not found, loading ASRA class instead.")
            # Return the ASRA class instead of the missing class
            return ASRA
        # Otherwise, call the original find_class method
        return pickle.Unpickler.find_class(self, module, name)

# Function to load the pickle file with the custom unpickler
def custom_pickle_load(file):
    with open(file, 'rb') as f:
        return CustomUnpickler(f).load()

for folder_path in BASE_PATH.iterdir():
    data_path = folder_path / "data.pickle"
    obj = custom_pickle_load(data_path)
    with data_path.open("wb") as f:
        pickle.dump(obj, f)
