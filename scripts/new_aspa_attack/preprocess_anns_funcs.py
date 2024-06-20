from typing import Optional, TYPE_CHECKING

from bgpy.simulation_engine import ASPA
from bgpy.simulation_framework.scenarios.preprocess_anns_funcs import (
    _get_valid_by_roa_ann,
    _find_shortest_non_adopting_path_general,
    forged_origin_export_all_hijack
)

if TYPE_CHECKING:
    from bgpy.as_graphs import AS
    from bgpy.simulation_framework.scenario import Scenario
    from bgpy.simulation_engine import Announcement as Ann, BaseSimulationEngine
    from bgpy.simulation_engine import Policy


def aspa_hijack(
    self_scenario: "Scenario",
    unprocessed_anns: tuple["Ann", ...],
    engine: Optional["BaseSimulationEngine"],
    prev_scenario: Optional["Scenario"],
) -> tuple["Ann", ...]:

    processed_anns = list()

    valid_ann = _get_valid_by_roa_ann(self_scenario.victim_asns, unprocessed_anns)

    if not any(
        issubclass(x, ASPA) for x in self_scenario.non_default_asn_cls_dict.values()
    ):
        raise ValueError("ASPA attack used against no ASPA ASes?")

    for ann in unprocessed_anns:
        # If the announcement is from the attacker
        if ann.invalid_by_roa:

            # Forged-origin hijack when attacker can get to input clique
            if _zero_adopter_path_to_input_clique(ann.origin, self_scenario, engine):
                # Make the AS path be just the victim
                processed_ann = ann.copy(
                    {
                        "as_path": (ann.origin, valid_ann.origin),
                        # Ann.copy overwrites seed_asn and traceback by default
                        # so include these here to make sure that doesn't happen
                        "seed_asn": ann.seed_asn,
                        "traceback_end": ann.traceback_end,
                    }
                )
                processed_anns.append(processed_ann)
                print("AAA!!!!!!")
            # Default to SP-EA attack
            else:

                print("BBBBB!!!!!!")
                shortest_as_path = _find_shortest_non_adopting_path_general(
                    valid_ann.origin, self_scenario, engine
                )
                # Default to an origin hijacking. With ASPA, this will sometimes work,
                # even at high adoption. ROV blocks it otherwise.
                # Without this, additionally, neighbor spoofing hijack will break
                # since you'll strip the attacker out of a path with only the attacker
                if shortest_as_path is None:
                    return forged_origin_export_all_hijack(
                        self_scenario, unprocessed_anns, engine, prev_scenario
                    )
                else:
                    # This can happen if the attacker is the shortest path
                    # See shortest_path_export_all_aspa_simple_provider test (27)
                    if shortest_as_path[0] == ann.as_path[0] and len(shortest_as_path) > 1:
                        shortest_as_path = shortest_as_path[1:]
                    processed_anns.append(
                        ann.copy(
                            {
                                "as_path": ann.as_path + shortest_as_path,
                                # Ann.copy overwrites seed_asn and traceback by default
                                # so include these here to make sure that doesn't happen
                                "seed_asn": ann.seed_asn,
                                "traceback_end": ann.traceback_end,
                            }
                        )
                    )
        else:
            processed_anns.append(ann)

    return tuple(processed_anns)


def _zero_adopter_path_to_input_clique(
    root_asn: int,
    self_scenario: "Scenario",
    engine: Optional["BaseSimulationEngine"],
) -> Optional[tuple[int, ...]]:
    """Finds the shortest non adopting path from the root asn

    Announcements from customers > peers > providers, since
    policies like ASPA and bgp-isec would reject announcements
    that are already going to customers, etc. So even if the path
    is longer, it's better to be accepted by going to a provider
    """

    AdoptPolicyCls = self_scenario.scenario_config.AdoptPolicyCls

    def get_policy(as_: "AS") -> type["Policy"]:
        return self_scenario.non_default_asn_cls_dict.get(  # type: ignore
            as_.asn, self_scenario.scenario_config.BasePolicyCls
        )

    assert engine, "mypy"
    root_as = engine.as_graph.as_dict[root_asn]

    def success(as_) -> bool:
        """Returns True if AS is input clique and not deploying ASPA"""

        return as_.input_clique and not issubclass(get_policy(as_), AdoptPolicyCls)

    def helper(root_as) -> bool:

        # End conditions

        # We're adopting, so this path doesn't work
        if issubclass(get_policy(root_as), AdoptPolicyCls):
            return False
        # We're not adopting, and input clique:
        elif success(root_as):
            assert not issubclass(get_policy(root_as), AdoptPolicyCls), "should never happen"
            return True
        # If any peers are input clique and not adopting
        elif any(success(peer_as) for peer_as in root_as.peers):
            return True
        # We've reached the top, we're not input clique (or we are adopting), and we've
        # checked all the peers, so this path doens't work
        elif len(root_as.providers) == 0:
            return False

        # Recursive loop
        for as_ in root_as.providers:
            if helper(as_):
                return True

        # We've gone all the way up on all of the providers, none work
        return False

    return helper(root_as)
