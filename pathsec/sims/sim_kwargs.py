import argparse
from multiprocessing import cpu_count
from pathlib import Path

from frozendict import frozendict
from bgpy.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import GraphFactory

# Set up argparse to handle command line arguments
parser = argparse.ArgumentParser(description="Run simulations with dynamic configurations.")
parser.add_argument("-n", "--num_trials", "--trials", dest="trials", type=int, default=1000, help="Number of trials to run")
parser.add_argument("--quick", action="store_true", help="Run a quick simulation with reduced parameters")

args = parser.parse_args()

# Define default kwargs using argparse results
default_kwargs = frozendict(
    {
        "percent_adoptions": (
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.5,
            0.8,
            0.99,
        ),
        "num_trials": 1 if args.quick else args.trials,  # Use trials here
        "parse_cpus": cpu_count() - 2,
        "python_hash_seed": 0,
    }
)

run_kwargs = frozendict(
    {
        "GraphFactoryCls": None if args.quick else GraphFactory,
        "graph_factory_kwargs" = {
            "y_axis_label_replacement_dict": {
                "PERCENT ATTACKER SUCCESS": "Percent Attacker Success"
            },
        }
    }
)

DIR = Path.home() / "Desktop" / "aspa_sims"
