from typing import Optional, TYPE_CHECKING

from bgpy.enums import Relationships
from bgpy.simulation_engine.policies.bgp import BGPPolicy

if TYPE_CHECKING:
    from bgpy.simulation_engine import Announcement as Ann


class PathSusAlgo5SimplePolicy(BGPPolicy):
    """Detects origin hijacks and drops them"""

    name: str = "PathSusAlgo5Simple"

    MIN_SUS_PATH_LEN = 5

    def _get_best_ann_by_gao_rexford(
        self: "BGPPolicy",
        current_ann: Optional["Ann"],
        new_ann: "Ann",
    ) -> "Ann":
        """Determines if the new ann > current ann by Gao Rexford"""

        assert new_ann is not None, "New announcement can't be None"

        if current_ann is None:
            return new_ann
        else:
            # Inspiration for this func refactor came from bgpsecsim
            # for func in self._gao_rexford_funcs:
            #     best_ann = func(current_ann, new_ann)
            #     if best_ann is not None:
            #         assert isinstance(best_ann, Ann), "mypy type check"
            #         return best_ann

            # Having this dynamic like above is literally 7x slower, resulting
            # in bottlenecks. Gotta do it the ugly way unfortunately
            if (
                new_ann.recv_relationship.value == Relationships.CUSTOMERS.value
                and current_ann.recv_relationship.value in (
                    Relationships.PROVIDERS.value,
                    Relationships.PEERS.value
                )
                and len(new_ann.as_path) > len(current_ann.as_path)
                and len(new_ann.as_path) >= self.MIN_SUS_PATH_LEN
            ):
                return new_ann
            else:
                ann = self._get_best_ann_by_local_pref(current_ann, new_ann)
                if ann:
                    return ann
                else:
                    ann = self._get_best_ann_by_as_path(current_ann, new_ann)
                    if ann:
                        return ann
                    else:
                        return self._get_best_ann_by_lowest_neighbor_asn_tiebreaker(
                            current_ann, new_ann
                        )
            raise Exception("No ann was chosen")


class PathSusAlgo4SimplePolicy(PathSusAlgo5SimplePolicy):
    """Detects origin hijacks and drops them"""

    name: str = "PathSusAlgo4Simple"

    MIN_SUS_PATH_LEN = 4


class PathSusAlgo3SimplePolicy(PathSusAlgo5SimplePolicy):
    """Detects origin hijacks and drops them"""

    name: str = "PathSusAlgo3Simple"

    MIN_SUS_PATH_LEN = 3
