from multiprocessing import cpu_count
from pathlib import Path
import sys

from frozendict import frozendict

from bgpy.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import GraphFactory


default_kwargs = frozendict(
    {
        "percent_adoptions": (
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.5,
            0.8,
            0.99,
            # Using only 1 AS not adopting causes extreme variance
            # SpecialPercentAdoptions.ALL_BUT_ONE,
        ),
        "num_trials": 1 if "quick" in str(sys.argv) else 40,
        "parse_cpus": cpu_count() - 2,
    }
)

run_kwargs = frozendict(
    {
        "GraphFactoryCls": None if "quick" in str(sys.argv) else GraphFactory,
    }
)

DIR = Path.home() / "Desktop" / "aspa_sims"
