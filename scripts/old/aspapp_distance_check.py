from collections import defaultdict
from pprint import pprint
from statistics import mean
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
        if asn in distances[input_clique_asn]:
            return
        min_provider_dist = MAX_DIST
        as_ = bgp_dag.as_dict[asn]
        for provider in as_.providers:
            provider_dist = distances[input_clique_asn].get(provider.asn, None)
            # We haven't calculated this yet
            if provider_dist is None:
                helper(provider.asn, input_clique_asn)
                provider_dist = distances[input_clique_asn][provider.asn]

            if provider_dist < min_provider_dist:
                min_provider_dist = provider_dist
        distances[input_clique_asn][asn] = min_provider_dist + 1

    for input_clique_as in tqdm(input_clique_ases, total=len(input_clique_ases)):
        distances[input_clique_as.asn][input_clique_as.asn] = 1
        for as_ in bgp_dag:
            helper(as_.asn, input_clique_as.asn)

    if False:
       for input_clique_asn, inner_dict in distances.items():
           print(f"input clique asn {input_clique_asn}")
           for asn, dist in inner_dict.items():
               print(f"{asn} {dist}")
               input()
    # pprint(distances)

    # Calculate the avg distance to each input clique AS for debugging
    avg_distances = dict()
    for input_clique_as in input_clique_ases:
        avg_distances[input_clique_as.asn] = mean(
            [x for x in distances[input_clique_as.asn].values() if x < MAX_DIST]
        )
    pprint(avg_distances)

    # calculate the min distance to ANY input clique AS
    min_distances = dict()
    for as_ in tqdm(bgp_dag, total=len(bgp_dag)):
        min_dist = MAX_DIST
        for input_clique_as in input_clique_ases:
            # When the AS has no conn to input clique, default to 0
            dist_to_input_clique_as = distances[input_clique_as.asn].get(as_.asn, MAX_DIST)
            if (
                dist_to_input_clique_as < min_dist
                and dist_to_input_clique_as < MAX_DIST
            ):
                min_dist = dist_to_input_clique_as
        if min_dist < MAX_DIST:
            min_distances[as_.asn] = min_dist
    # Now calculate how many distances are >= 5
    total = len(bgp_dag)
    too_long_total = 0
    for asn, min_distance in tqdm(min_distances.items(), total=len(min_distances)):
        if min_distance >= 5:
            too_long_total += 1
    print(f"Out of {total}, {too_long_total} are too long for min")

    # Now calculate the MAX distances from each AS to any input clique
    max_distances = dict()
    for as_ in tqdm(bgp_dag, total=len(bgp_dag)):
        max_dist = 0
        for input_clique_as in input_clique_ases:
            # When the AS has no conn to input clique, default to 0
            dist_to_input_clique_as = distances[input_clique_as.asn].get(as_.asn, 0)
            if (
                dist_to_input_clique_as > max_dist
                and dist_to_input_clique_as < MAX_DIST
            ):
                max_dist = dist_to_input_clique_as
        if max_dist > 0:
            max_distances[as_.asn] = max_dist

    print(f"{len(max_distances)} have routes to input clique")

    # Now calculate how many distances are >= 5
    total = len(bgp_dag)
    too_long_total = 0
    for asn, max_distance in tqdm(max_distances.items(), total=len(max_distances)):
        if max_distance >= 5:
            too_long_total += 1
    print(f"Out of {total}, {too_long_total} are too long")


if __name__ == "__main__":
    main()
