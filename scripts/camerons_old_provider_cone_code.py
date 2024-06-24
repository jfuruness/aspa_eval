from tqdm import tqdm

import random
from bgpy.as_graphs.base.links import CustomerProviderLink as CPLink
from bgpy.as_graphs import CAIDAASGraphConstructor, AS
from bgpy.as_graphs import ASGraphInfo, CAIDAASGraph
from bgpy.enums import ASGroups, Relationships



class ProviderConeComputation:
    """Compute provider cones for every AS in the CAIDA topology."""

    def __init__(self):

        self.engine = CAIDAASGraphConstructor(tsv_path=None).run()
        # Initialize
        self.provider_cones = dict()
        for as_obj in tqdm(self.engine, total=len(self.engine), desc="cones"):
            self.provider_cones[as_obj.asn] = set()

    def get_cone(self, as_obj):
        """Compute a provider cone for a single AS"""
        if as_obj.input_clique or len(self.provider_cones[as_obj.asn]) > 0:
            return
        asns_in_cone = set()
        for provider_obj in as_obj.providers:
            if len(self.provider_cones[provider_obj.asn]) == 0:
                self.get_cone(provider_obj)
            asns_in_cone = asns_in_cone.union(self.provider_cones[provider_obj.asn])
            asns_in_cone.add(provider_obj.asn)
        self.provider_cones[as_obj.asn] = asns_in_cone

    def get_all_cones(self):
        """Populate self.provider_cones for every AS"""
        for as_obj in self.engine:
            self.get_cone(as_obj)


def test_provider_cones():
    a = ProviderConeComputation()
    a.engine.ases[0].providers = (a.engine.ases[1], a.engine.ases[2])
    a.engine.ases[1].providers = tuple()
    a.engine.ases[2].providers = tuple()
    a.get_cone(a.engine.ases[0])
    if len(a.provider_cones[a.engine.ases[0].asn]) != 2:
        print("Error 1")
        exit()
    a = ProviderConeComputation()
    a.engine.ases[0].providers = (a.engine.ases[1], a.engine.ases[2])
    a.engine.ases[1].providers = tuple()
    a.engine.ases[2].providers = (a.engine.ases[3],)
    a.engine.ases[3].providers = tuple()
    a.get_cone(a.engine.ases[0])
    if len(a.provider_cones[a.engine.ases[0].asn]) != 3:
        print("Error 2")
        exit()


if __name__ == "__main__":
    a = ProviderConeComputation()
    a.get_all_cones()
    provider_cone_dict = a.provider_cones
    from statistics import mean, median

    print(mean(len(x) for x in provider_cone_dict.values()))
    print(median(len(x) for x in provider_cone_dict.values()))

    """
    h_max = 200
    s_max = 0
    histogram = [0 for i in range(h_max)]
    for asn, cone in a.provider_cones.items():
        if len(cone) < h_max:
            histogram[len(cone)] += 1
        if len(cone) > s_max:
            s_max = len(cone)
    print("Number of provider cones of size x")
    for i in range(h_max):
        print(f"{i}\t{histogram[i]}")
    print("Max:", s_max)
    """
