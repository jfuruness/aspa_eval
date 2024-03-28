from bgpy.simulation_engine import ROV
from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


class ROVWOriginHijack(ROV):
    name = "ROV & Origin Hijack"


class ROVWOriginSpoofingHijack(ROV):
    name = "ROV & Origin Spoofing Hijack"


def run_origin_spoofing_hijack_sim():
    """Runs sim for an origin hijack"""

    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROVWOriginHijack,
                    preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
                ),
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROVWOriginSpoofingHijack,
                    preprocess_anns_func=preprocess_anns_funcs.origin_spoofing_hijack,
                ),
            ]
        ),
        output_dir=DIR / "origin_spoofing_hijack",
        **default_kwargs,  # type: ignore
    )
    sim.run(**run_kwargs)
