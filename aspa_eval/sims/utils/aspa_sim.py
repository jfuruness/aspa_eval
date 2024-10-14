
from multiprocessing import cpu_count
from pathlib import Path

from bgpy.shared.constants import DIRS, SINGLE_DAY_CACHE_DIR
from bgpy.shared.enums import ASGroups
from bgpy.simulation_framework import AccidentalRouteLeak, ScenarioConfig, Simulation
from frozendict import frozendict


class ASPASim(Simulation):
    """SimulationClass customized for ASPA sims"""

    def __init__(self, *args, **kwargs) -> None:
        kwargs["python_hash_seed"] = 0
        kwargs["as_graph_constructor_kwargs"] = frozendict(
            {
                "as_graph_collector_kwargs": frozendict(
                    {
                        "cache_dir": SINGLE_DAY_CACHE_DIR,
                        "dl_time": datetime(2024, 4, 5, 15, 3),
                    }
                ),
                "as_graph_kwargs": frozendict(
                    {
                        # When no ASNs are stored, .9gb/core
                        # When one set of cones is stored, 1.6gb/core
                        # When both sets of cones are stored, 2.3gb/core
                        # Unfortunately, we need both, since we use BGP-iSec
                        # and also use customer cones for ASRA
                        "store_customer_cone_size": True,
                        "store_customer_cone_asns": True,
                        "store_provider_cone_size": True,
                        "store_provider_cone_asns": True,
                    }
                ),
                "tsv_path": None,  # Path.home() / "Desktop" / "caida.tsv",
            }
        )
        total_cpus = cpu_count()
        MAX_CPUS = 100
        if total_cpus > MAX_CPUS:
            kwargs["parse_cpus"] = min(kwargs.get("parse_cpus", total_cpus), MAX_CPUS)
        super().__init__(*args, **kwargs)

    @property
    def default_sim_name(self) -> str:
        return (
            f"{self.scenario_configs[0].ScenarioCls.__name__.lower()}_"
            f"{self.scenario_configs[0].attacker_subcategory_attr}_"
            f"{self.scenario_configs[0].num_attackers}_attackers"
        )

    @property
    def default_output_dir(self) -> Path:
        return Path(DIRS.user_desktop_dir) / "sims" / "aspa_sims" / self.sim_name

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
