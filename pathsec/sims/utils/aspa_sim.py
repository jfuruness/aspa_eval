from typing import TYPE_CHECKING

from bgpy.shared.enums import ASGroups
from bgpy.simulation_framework import AccidentalRouteLeak, ScenarioConfig, Simulation

if TYPE_CHECKING:
    from pathlib import Path


class ASPASim(Simulation):
    """SimulationClass customized for ASPA sims"""

    def __init__(self, *args, **kwargs) -> None:
        kwargs["python_hash_seed"] = 0
        super().__init__(*args, **kwargs)

    @property
    def default_sim_name(self) -> str:
        return "aspa_sims"

    @property
    def default_output_dir(self) -> "Path":
        return (
            super().default_output_dir
            / self.scenario_configs[0].ScenarioCls.__name__.lower()
            / self.scenario_configs[0].attacker_subcategory_attr
            / f"{self.scenario_configs[0].num_attackers}_attackers"
        )

    def _get_filtered_scenario_configs(
        self, scenario_configs: tuple["ScenarioConfig", ...]
    ) -> tuple[ScenarioConfig, ...]:
        """Removes confs that aren't applicable for this run for speed"""

        filtered_confs = list()
        for conf in scenario_configs:
            # Only run OTC with route leaks
            if (
                conf.ScenarioCls != AccidentalRouteLeak
                and "OTC" in conf.AdoptPolicyCls.name
            ):
                continue
            # EdgeFilter isn't applicable when attacker isn't at the edge
            elif (
                conf.attacker_subcategory_attr
                in (
                    ASGroups.TRANSIT.value,
                    ASGroups.ETC.value,
                    ASGroups.INPUT_CLIQUE.value,
                )
                and "Edge" in conf.AdoptPolicyCls.name
            ):
                continue
            # Pathend and BGPSec variants do nothing against route leaks
            elif conf.ScenarioCls == AccidentalRouteLeak and (
                "Path-End" in conf.AdoptPolicyCls.name
                or "BGPSec" in conf.AdoptPolicyCls.name
                or "BGP-iSec" in conf.AdoptPolicyCls.name
            ):
                continue
            else:
                filtered_confs.append(conf)

        return tuple(filtered_confs)
