from bgpy.simulation_engine import ASPA, ROV

from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    preprocess_anns_funcs,
    ScenarioConfig,
)

from .sim_kwargs import DIR, default_kwargs, run_kwargs


def run_strongest_attack_sim():

    sim = Simulation(
        scenario_configs=tuple(
            [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ASPA,
                    preprocess_anns_func=func,
                    scenario_label=f"{func.__name__} (ASPA)",
                )
                for func in (
                    preprocess_anns_funcs.forged_origin_export_all_hijack,
                    preprocess_anns_funcs.shortest_path_export_all_hijack,
                )
            ] + [
                ScenarioConfig(
                    ScenarioCls=PrefixHijack,
                    AdoptPolicyCls=ROV,
                    preprocess_anns_func=(
                        preprocess_anns_funcs.forged_origin_export_all_hijack
                    ),
                    scenario_label="Forged-Origin (ROV)",
                )
            ]
        ),
        output_dir=DIR / "strongest_attack",
        **default_kwargs,  # type: ignore
    )
    sim.run(**run_kwargs)  # type: ignore
