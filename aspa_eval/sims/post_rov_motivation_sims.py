import json
import os
import random
from functools import partial
from pathlib import Path
from statistics import mean

from bgpy.simulation_engine import ROV
from bgpy.simulation_framework import (
    ForgedOriginPrefixHijack,
    PrefixHijack,
    ScenarioConfig,
    SubprefixHijack,
)
from frozendict import frozendict
from rov_collector import Source as ROVSource
from rov_collector import rov_collector_classes

from .utils import ASPASim


def max_prob_func(
    asn, info_list, allowed_sources=frozenset([x.value for x in ROVSource])
) -> float:
    """Returns max probability for a given ASN"""
    prob_to_adopt: float = 0
    for info in info_list:
        if info["source"] in allowed_sources:
            prob_to_adopt = max(prob_to_adopt, float(info["percent"]))
    return prob_to_adopt


def mean_prob_func(asn, info_list) -> float:
    """Returns avg prob for a given ASN"""

    return mean(float(x["percent"]) for x in info_list)


def mean_when_measured_prob_func(asn, info_list) -> float:
    """Returns avg prob for a given ASN when ASN doesn't measure as 0

    Sometimes these sources will list an AS as 0 simply because they
    don't measure it
    """

    return mean(float(x["percent"]) for x in info_list if float(x["percent"]) > 0)


def get_real_world_rov_asn_cls_dict(
    json_path: Path = Path.home() / "Desktop" / "rov_info.json",
    requests_cache_db_path: Path | None = None,
    prob_func=max_prob_func,
) -> frozendict[int, type[ROV]]:
    if not json_path.exists():
        for CollectorCls in rov_collector_classes:
            CollectorCls(
                json_path=json_path,
                requests_cache_db_path=requests_cache_db_path,
            ).run()

    python_hash_seed = os.environ.get("PYTHONHASHSEED")
    if str(python_hash_seed) != "0":
        raise RuntimeError("Set PYTHONHASHSEED to 0 for reproducibility")
    if python_hash_seed:
        random.seed(int(python_hash_seed))

    with json_path.open() as f:
        data = json.load(f)
        hardcoded_dict = dict()
        if prob_func == mean_prob_func:
            print(  # noqa: T201
                "Method isn't realistic since most data "
                "sources only have a few ASes, use mean_when_measured instead"
            )
        for asn, info_list in data.items():
            if random.random() * 100 < prob_func(asn, info_list):  # noqa: S311
                hardcoded_dict[int(asn)] = ROV

    return frozendict(hardcoded_dict)


# {'APNIC', 'ROVISTA', 'isbgpsafeyet', 'Friends', 'rov.rpki.net', 'Revisiting RPKI'}

prob_funcs = list()


############################
# Funcs from Friends paper #
############################


def max_when_hayas_paper(asn, info_list, valid_categories=frozenset([2, 3, 6, 7])):
    prob_to_adopt: float = 0
    for info in info_list:
        if (
            info["source"] == ROVSource.FRIENDS.value
            and int(info["metadata"]["category"]) in valid_categories
        ):
            prob_to_adopt = max(prob_to_adopt, float(info["percent"]))
    return prob_to_adopt


for valid_categories_subset in [
    # frozenset([2, 3, 6, 7]),  # Don't need for paper
    frozenset([3, 6, 7]),
    # frozenset([6, 7]),  # Don't need for paper
    # frozenset([7]),  # Don't need for paper
]:
    new_func = partial(max_when_hayas_paper, valid_categories=valid_categories_subset)
    cat_str = "".join(str(x) for x in sorted(valid_categories_subset))
    new_func.__name__ = f"friends_{cat_str}"  # type: ignore
    prob_funcs.append(new_func)

###########################
# Funcs from other papers #
###########################

not_in_paper = (ROVSource.TMA, ROVSource.ROV_RPKI_NET)
for Src in [x for x in ROVSource if x not in (ROVSource.FRIENDS, *not_in_paper)]:
    new_func = partial(max_prob_func, allowed_sources=frozenset([Src.value]))
    new_func.__name__ = Src.value  # type: ignore
    prob_funcs.append(new_func)

#############
# Agg funcs #
#############

# prob_funcs.extend([max_prob_func, mean_prob_func, mean_when_measured_prob_func])  # Don't need for paper  # type: ignore


def run_post_rov_motivation_sim(prob_func):
    """ya, it's janky af. Sorry."""

    rov_asns_dict = get_real_world_rov_asn_cls_dict(prob_func=prob_func)

    # Simulation for the paper
    sim = ASPASim(
        scenario_configs=(
            ScenarioConfig(
                ScenarioCls=ForgedOriginPrefixHijack,
                AdoptPolicyCls=ROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
                scenario_label="ROV (Forged-Origin Export-All Hijack)",
            ),
            ScenarioConfig(
                ScenarioCls=SubprefixHijack,
                AdoptPolicyCls=ROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
                scenario_label="ROV (Subprefix Hijack)",
            ),
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                AdoptPolicyCls=ROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
                scenario_label="ROV (Prefix Hijack)",
            ),
        ),
        sim_name=f"rov_deployment_{prob_func.__name__}",
    )
    sim.run()
