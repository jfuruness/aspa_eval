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
    preprocess_anns_funcs
)


from rov_collector import rov_collector_classes


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


def get_real_world_rov_asn_cls_dict(
    json_path: Path = Path.home() / "Desktop" / "rov_info.json",
    requests_cache_db_path: Optional[Path] = None,
    method: str = "",  # really should be an enum
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
        if method == "avg" or method == "mean":
            print(
                f"Method {method} isn't realistic since most data "
                "sources only have a few ASes, use avg_when_measured instead"
            )
        for asn, info_list in data.items():
            prob_to_adopt: float = 0

            if method == "max":
                prob_to_adopt: float = 0
                # Calculate max_percent for each ASN
                for info in info_list:
                    prob_to_adopt = max(prob_to_adopt, float(info["percent"]))

            elif method == "avg" or method == "mean":
                # When ROV is measured take the average of those
                prob_to_adopt = mean(float(x["percent"]) for x in info_list)
            elif method == "avg_when_measured" or method == "mean_when_measured":
                # When ROV is measured take the average of those
                prob_to_adopt = mean(
                    float(x["percent"]) for x in info_list if float(x["percent"]) > 0
                )

            else:
                raise NotImplementedError

            if random.random() * 100 < prob_to_adopt:
                hardcoded_dict[int(asn)] = RealROVSimplePolicy

    return frozendict(hardcoded_dict)


def run_post_rov_motivation_sim(method):
    """ya, it's janky af. Sorry."""

    rov_asns_dict = get_real_world_rov_asn_cls_dict(method=method)

    # Simulation for the paper
    sim = Simulation(
        scenario_configs=(
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                preprocess_anns_func=preprocess_anns_funcs.origin_spoofing_hijack,
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
        output_dir=DIR / f"rov_deployment_{method}",
        **default_kwargs
    )
    run_kwargs["graph_factory_kwargs"] = {
        "y_axis_label_replacement_dict": {
            "PERCENT ATTACKER SUCCESS": "Percent Attacker Success"
        },
        "x_axis_label_replacement_dict": {
            "Percent Adoption": "Percent of Additional Adoption"
        },
    }

    sim.run(**run_kwargs)
