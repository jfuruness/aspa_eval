from collections import defaultdict
from tqdm import tqdm

from bgpy.as_graphs import CAIDAASGraphConstructor
from bgpy.enums import ASGroups

# This is also a placeholder for when there is no route
MAX_DIST = 1000000


def main():
    bgp_dag = CAIDAASGraphConstructor(tsv_path=None).run()
    input_clique_ases = bgp_dag.as_groups[ASGroups.INPUT_CLIQUE.value]
    # input_clique_asn: {asn: distance}
    distances = defaultdict(dict)

    def helper(asn, input_clique_asn):
        min_provider_dist = MAX_DIST
        as_ = bgp_dag.as_dict[asn]
        for provider in as_.providers:
            provider_dist = distances[input_clique_asn].get(provider.asn, None)
            # We haven't calculated this yet
            if provider_dist is None:
                helper(provider.asn, input_clique_asn)
                provider_dist = distances[input_clique_asn].get(provider.asn, None)

            if provider_dist < min_provider_dist:
                min_provider_dist = provider_dist
        distances[input_clique_asn][asn] = min_provider_dist + 1

    for input_clique_as in tqdm(input_clique_ases, total=len(input_clique_ases)):
        for as_ in bgp_dag:
            helper(as_.asn, input_clique_as.asn)

    # Now calculate the MAX distances from each AS to any input clique
    max_distances = dict()
    for as_ in tqdm(bgp_dag, total=len(bgp_dag)):
        max_dist = 0
        for input_clique_as in input_clique_ases:
            # When the AS has no conn to input clique, default to 0
            dist_to_input_clique_as = distances[input_clique_as.asn].get(as_.asn, 0)
            if (
                dist_to_input_clique_as > max_dist
                and dist_to_input_clique_as != MAX_DIST
            ):
                max_dist = dist_to_input_clique_as
        max_distances[as_.asn] = max_dist

    print(f"{len(max_distances)} have routes to input clique")

    # Now calculate how many distances are >= 5
    total = len(bgp_dag)
    too_long_total = 0
    for asn, max_distance in tqdm(max_distances, total=len(max_distances)):
        if max_distance >= 5:
            too_long_total += 1
    print(f"Out of {total}, {too_long_total} are too long")


if __name__ == "__main__":
    main()
