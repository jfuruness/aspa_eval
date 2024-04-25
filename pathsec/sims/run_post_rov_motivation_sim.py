import json
from pathlib import Path
import random
import os
from statistics import mean
from typing import Optional

from frozendict import frozendict

from bgpy.simulation_engine import ROVSimplePolicy

from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    SubprefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs,
)


from rov_collector import rov_collector_classes, Source as ROVSource


from .sim_kwargs import DIR, default_kwargs, run_kwargs


class RealROVSimplePolicy(ROVSimplePolicy):
    name = "RealROV"


class PrefixHijackROV(ROVSimplePolicy):
    name = "Prefix Hijack (ROV)"


class SubprefixHijackROV(ROVSimplePolicy):
    name = "Subprefix Hijack (ROV)"


class OriginHijackROV(ROVSimplePolicy):
    name = "Origin Hijack (ROV)"


class NeighborSpoofingHijackROV(ROVSimplePolicy):
    name = "Neighbor Spoofing Hijack (ROV)"


def max_prob_func(
    asn,
    info_list,
    allowed_sources=frozenset([x.value for x in ROVSource])
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
    requests_cache_db_path: Optional[Path] = None,
    prob_func=max_prob_func,
) -> frozendict[int, type[RealROVSimplePolicy]]:
    if not json_path.exists():
        for CollectorCls in rov_collector_classes:
            CollectorCls(
                json_path=json_path,
                requests_cache_db_path=requests_cache_db_path,
            ).run()  # type: ignore

    python_hash_seed = os.environ.get("PYTHONHASHSEED")
    if str(python_hash_seed) != "0":
        raise Exception("Set PYTHONHASHSEED to 0 for reproducibility")
    if python_hash_seed:
        random.seed(int(python_hash_seed))

    with json_path.open() as f:
        data = json.load(f)
        hardcoded_dict = dict()
        if prob_func == mean_prob_func:
            print(
                f"Method isn't realistic since most data "
                "sources only have a few ASes, use mean_when_measured instead"
            )
        for asn, info_list in data.items():
            if random.random() * 100 < prob_func(asn, info_list):
                hardcoded_dict[int(asn)] = RealROVSimplePolicy

    return frozendict(hardcoded_dict)


def run_post_rov_motivation_sim(prob_func):
    """ya, it's janky af. Sorry."""

    rov_asns_dict = get_real_world_rov_asn_cls_dict(prob_func=prob_func)

    # Simulation for the paper
    sim = Simulation(
        scenario_configs=(
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                preprocess_anns_func=preprocess_anns_funcs.neighbor_spoofing_hijack,
                AdoptPolicyCls=NeighborSpoofingHijackROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
            ),
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
                AdoptPolicyCls=OriginHijackROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
            ),
            ScenarioConfig(
                ScenarioCls=SubprefixHijack,
                AdoptPolicyCls=SubprefixHijackROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
            ),
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                AdoptPolicyCls=PrefixHijackROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
            ),
        ),
        output_dir=DIR / f"rov_deployment" / prob_func.__name__,
        **default_kwargs,  # type: ignore
    )
    new_run_kwargs = dict(run_kwargs)
    new_run_kwargs["graph_factory_kwargs"]["x_axis_label_replacement_dict"] = {
        "Percent Adoption": "Percent of Additional Adoption"
    }
    sim.run(**new_run_kwargs)
