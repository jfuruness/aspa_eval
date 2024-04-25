from functools import partial
from pprint import pprint  # noqa
import time

from pathsec.sims.run_post_rov_motivation_sim import (
    run_post_rov_motivation_sim,
    max_prob_func,
    mean_prob_func,
    mean_when_measured_prob_func,
)
from rov_collector import Source as ROVSource


# {'APNIC', 'ROVISTA', 'isbgpsafeyet', 'Friends', 'rov.rpki.net', 'Revisiting RPKI'}

prob_funcs = list()


############################
# Funcs from Friends paper #
############################

def max_when_hayas_paper(asn, info_list, valid_categories=frozenset([2, 3, 6, 7])):
    prob_to_adopt: float = 0
    for info in info_list:
        if info["source"] == ROVSource.FRIENDS.value:
            if int(info["metadata"]["category"]) in valid_categories:
                prob_to_adopt = max(prob_to_adopt, float(info["percent"]))
    return prob_to_adopt


for valid_categories_subset in [
    frozenset([2, 3, 6, 7]),
    frozenset([3, 6, 7]),
    frozenset([6, 7]),
    frozenset([7]),
]:
    new_func = partial(max_when_hayas_paper, valid_categories=valid_categories_subset)
    cat_str = ''.join(str(x) for x in sorted(valid_categories_subset))
    new_func.__name__ = f"friends_{cat_str}"
    prob_funcs.append(new_func)

###########################
# Funcs from other papers #
###########################

for Src in [x for x in ROVSource if x != ROVSource.FRIENDS]:
    new_func = partial(max_prob_func, allowed_sources=frozenset([Src.value]))
    new_func.__name__ = Src.value
    prob_funcs.append(new_func)

#############
# Agg funcs #
#############

prob_funcs.extend([max_prob_func, mean_prob_func, mean_when_measured_prob_func])

for i, func in enumerate(prob_funcs):
    start = time.perf_counter()
    print(f"Running {func.__name__}")
    run_post_rov_motivation_sim(func)
    print(
        f"{func.__name__} ({i + 1}/{len(prob_funcs)} "
        f"ran in {time.perf_counter() - start}s"
    )
