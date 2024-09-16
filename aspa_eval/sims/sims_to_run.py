from .adoption_scenario_sims import (
    forged_origin_hijack_adoption_scenarios_sim,
    route_leak_adoption_scenarios_sim,
)
from .first_asn_stripping_sims import first_asn_stripping_sim
from .forged_origin_sims import (
    forged_origin_edge_10_attackers_sim,
    forged_origin_edge_sim,
    forged_origin_etc_sim,
)
from .route_leak_sims import (
    route_leak_mh_sim,
    route_leak_transit_sim,
)
from .shortest_path_sims import (
    shortest_path_edge_10_attackers_sim,
    shortest_path_edge_sim,
    shortest_path_etc_sim,
)

SIMS_TO_RUN = (
    first_asn_stripping_sim,
    forged_origin_edge_sim,
    forged_origin_edge_10_attackers_sim,
    forged_origin_etc_sim,
    route_leak_mh_sim,
    route_leak_transit_sim,
    shortest_path_edge_sim,
    shortest_path_edge_10_attackers_sim,
    shortest_path_etc_sim,
    forged_origin_hijack_adoption_scenarios_sim,
    route_leak_adoption_scenarios_sim,
)