from dataclasses import replace
import time

from bgpy.shared.enums import ASGroups
from bgpy.simulation_engine import ROV, ASPA, ASPAwN
from bgpy.simulation_framework import ForgedOriginPrefixHijack, ShortestPathPrefixHijack, ScenarioConfig, AccidentalRouteLeak

from aspa_eval.scenarios import ShortestPathCustomerConeHijack
from aspa_eval.sims.utils import ASPASim


hijack_sim = ASPASim(
    scenario_configs=[
        ScenarioConfig(
            AdoptPolicyCls=ROV,
            ScenarioCls=ForgedOriginPrefixHijack,
            scenario_label="Forged Origin (ROV)"
        ),
        ScenarioConfig(
            AdoptPolicyCls=ASPA,
            ScenarioCls=ForgedOriginPrefixHijack,
            scenario_label="Forged Origin (ASPA)"
        ),
        ScenarioConfig(
            AdoptPolicyCls=ASPA,
            ScenarioCls=ShortestPathPrefixHijack,
            scenario_label="Shortest Path (ASPA)"
        ),
    ],
    sim_name="ndss_aspa_attacks"
)
cc_sim = ASPASim(
    scenario_configs=[
        ScenarioConfig(
            AdoptPolicyCls=ASPA,
            ScenarioCls=ShortestPathCustomerConeHijack,
            scenario_label="Shortest Path (ASPA)",
            attacker_subcategory_attr=ASGroups.ETC.value,
        ),
        ScenarioConfig(
            AdoptPolicyCls=ASPAwN,
            ScenarioCls=ShortestPathCustomerConeHijack,
            scenario_label="Shortest Path (ASPAwN)",
            attacker_subcategory_attr=ASGroups.ETC.value,
        ),
    ],
    sim_name="ndss_aspawn"
)

leak_sim = ASPASim(
    scenario_configs=[
        ScenarioConfig(
            AdoptPolicyCls=ROV,
            ScenarioCls=AccidentalRouteLeak,
            scenario_label="ROV",
            attacker_subcategory_attr=ASGroups.MULTIHOMED.value
        ),
        ScenarioConfig(
            AdoptPolicyCls=ASPA,
            ScenarioCls=AccidentalRouteLeak,
            scenario_label="ASPA/OTC",
            attacker_subcategory_attr=ASGroups.MULTIHOMED.value
        ),
    ],
    sim_name="ndss_leaks"
)


# NOTE: Adoption scenarios can just be re-used from the paper
start = time.perf_counter()
# hijack_sim.run()
print(f"{time.perf_counter() - start}s for hijack sim")  # noqa: T201

start = time.perf_counter()
# cc_sim.run()
print(f"{time.perf_counter() - start}s for cc sim")  # noqa: T201

start = time.perf_counter()
leak_sim.run()
print(f"{time.perf_counter() - start}s for leak sim")  # noqa: T201
