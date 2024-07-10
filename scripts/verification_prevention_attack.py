
from __future__ import print_function
import random
from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.as_graphs import CAIDAASGraphConstructor, AS
from bgpy.as_graphs import ASGraphInfo, CAIDAASGraph
from bgpy.enums import ASGroups, Relationships


def get_cone(
    self, rel_attr: str = Relationships.PROVIDERS.name.lower()
) -> dict[int, set[int]]:
    cone_dict = dict()
    for as_obj in self:
        if as_obj.asn not in cone_dict:
            cone: set[int] = get_cone_helper(self, as_obj, cone_dict, rel_attr)
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
            if neighbor.asn not in cone_dict:
                get_cone_helper(self, neighbor, cone_dict, rel_attr)
            cone_dict[as_obj.asn].update(cone_dict[neighbor.asn])
    return cone_dict[as_obj.asn]


def main():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    edge_ases = bgp_dag.as_groups[ASGroups.MULTIHOMED.value]
    edge_ases = bgp_dag.as_groups[ASGroups.STUBS_OR_MH.value]
    provider_cone_dict = get_cone(
        bgp_dag, rel_attr=Relationships.PROVIDERS.name.lower()
    )
    provider_cone_dict = {k: frozenset(v) for k, v in provider_cone_dict.items()}
    #from sys import getsizeof
    #total = 0
    #for cone in provider_cone_dict.values():
    #    input(getsizeof(cone))
    #    total += getsizeof(cone)

    from sys import getsizeof, stderr
    from itertools import chain
    from collections import deque
    try:
        from reprlib import repr
    except ImportError:
        pass

    def total_size(o, handlers={}, verbose=False):
        """ Returns the approximate memory footprint an object and all of its contents.

        Automatically finds the contents of the following builtin containers and
        their subclasses:  tuple, list, deque, dict, set and frozenset.
        To search other containers, add handlers to iterate over their contents:

            handlers = {SomeContainerClass: iter,
                        OtherContainerClass: OtherContainerClass.get_elements}

        """
        dict_handler = lambda d: chain.from_iterable(d.items())
        all_handlers = {tuple: iter,
                        list: iter,
                        deque: iter,
                        dict: dict_handler,
                        set: iter,
                        frozenset: iter,
                       }
        all_handlers.update(handlers)     # user handlers take precedence
        seen = set()                      # track which object id's have already been seen
        default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

        def sizeof(o):
            if id(o) in seen:       # do not double count the same object
                return 0
            seen.add(id(o))
            s = getsizeof(o, default_size)

            if verbose:
                print(s, type(o), repr(o), file=stderr)

            for typ, handler in all_handlers.items():
                if isinstance(o, typ):
                    s += sum(map(sizeof, handler(o)))
                    break
            return s

        return sizeof(o)
    from pprint import pprint
    input(total_size(provider_cone_dict))
    for asn, cone in provider_cone_dict.items():
        break
        print(asn)
        pprint(cone)
        input()
    total = 0
    trials = 10000
    for _ in range(trials):
        attacker, victim = random.sample(edge_ases, 2)
        for provider in attacker.providers:
            if provider.asn in provider_cone_dict[victim.asn]:
                total += 1
                break
    from statistics import mean, median

    print(mean(len(x) for x in provider_cone_dict.values()))
    print(median(len(x) for x in provider_cone_dict.values()))

    print(f"{total}/{trials}")


def test_me():
    as_graph_info = ASGraphInfo(
        customer_provider_links=frozenset(
            [
                CPLink(provider_asn=1, customer_asn=2),
                CPLink(provider_asn=1, customer_asn=3),
                CPLink(provider_asn=1, customer_asn=4),
                CPLink(provider_asn=2, customer_asn=4),
                CPLink(provider_asn=3, customer_asn=4),
                CPLink(provider_asn=4, customer_asn=5),
                CPLink(provider_asn=1, customer_asn=6),
                CPLink(provider_asn=2, customer_asn=6),
                CPLink(provider_asn=3, customer_asn=6),
                CPLink(provider_asn=8, customer_asn=7),
                CPLink(provider_asn=9, customer_asn=7),
                CPLink(provider_asn=10, customer_asn=7),
                CPLink(provider_asn=11, customer_asn=10),
                CPLink(provider_asn=12, customer_asn=10),
            ]
        ),
    )
    as_graph = CAIDAASGraph(as_graph_info=as_graph_info)
    provider_cone_dict = get_cone(
        as_graph, rel_attr=Relationships.PROVIDERS.name.lower()
    )
    from pprint import pprint

    pprint(provider_cone_dict)


if __name__ == "__main__":
    # test_me()
    main()
