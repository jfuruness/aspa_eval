from random import random

from bgpy.as_graphs import CAIDAASGraphConstructor, AS
from bgpy.enums import ASGroups, Relationships


def get_cone(
    self, rel_attr: str = Relationships.PROVIDERS.value
) -> dict[int, set[int]]:
    cone_dict = dict()
    for as_obj in self:
        cone: set[int] = get_cone_helper(as_obj, cone_dict)
        cone_dict[as_obj.asn] = cone
    return cone_dict


def get_cone_helper(
    self,
    as_obj: AS,
    cone_dict: dict[int, set[int]],
    rel_attr: str,
) -> set[int]:
    """Recursively determines the cone size of an as"""

    if as_obj.asn in cone_dict:
        return cone_dict[as_obj.asn]
    else:
        cone_dict[as_obj.asn] = set()
        for neighbor in getattr(as_obj, rel_attr):
            cone_dict[as_obj.asn].add(neighbor.asn)
            get_cone_helper(neighbor, cone_dict, rel_attr)
            cone_dict[as_obj.asn].update(cone_dict[neighbor.asn])
    return cone_dict[as_obj.asn]


def main():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    edge_ases = bgp_dag.as_groups[ASGroups.MULTIHOMED.value]
    provider_cone_dict = get_cone(bgp_dag, rel_attr=Relationships.PROVIDERS.value)
    total = 0
    trials = 1000
    for _ in range(trials):
        attacker, victim = random.sample(edge_ases, 2)
        for provider in attacker.providers:
            if provider.asn in provider_cone_dict[victim.asn]:
                total += 1
                break

    print(f"{total}/{trials}")


if __name__ == "__main__":
    main()
