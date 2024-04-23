import json
from multiprocessing import cpu_count
from pathlib import Path
import random
import os
from typing import Optional

from frozendict import frozendict

from bgpy.simulation_engine import ROVSimplePolicy

from bgpy.enums import SpecialPercentAdoptions
from bgpy.simulation_framework import (
    Simulation,
    PrefixHijack,
    ScenarioConfig,
    preprocess_anns_funcs
)


from rov_collector import rov_collector_classes


class RealROVSimplePolicy(ROVSimplePolicy):
    name = "RealROV"

class PrefixHijackROV(ROVSimplePolicy):
    name = "Prefix Hijack (ROV)"

class OriginHijackROV(ROVSimplePolicy):
    name = "Origin Hijack (ROV)"



def get_real_world_rov_asn_cls_dict(
    json_path: Path = Path.home() / "Desktop" / "rov_info.json",
    requests_cache_db_path: Optional[Path] = None,
) -> frozendict[int, type[RealROVSimplePolicy]]:
    if not json_path.exists():
        for CollectorCls in rov_collector_classes:
            CollectorCls(
                json_path=json_path,
                requests_cache_db_path=requests_cache_db_path,
            ).run()  # type: ignore

    python_hash_seed = os.environ.get("PYTHONHASHSEED")
    if python_hash_seed:
        random.seed(int(python_hash_seed))

    with json_path.open() as f:
        data = json.load(f)
        hardcoded_dict = dict()
        for asn, info_list in data.items():
            max_percent: float = 0
            # Calculate max_percent for each ASN
            for info in info_list:
                max_percent = max(max_percent, float(info["percent"]))

            # Use max_percent as the probability for inclusion
            if random.random() * 100 < max_percent:
                hardcoded_dict[int(asn)] = RealROVSimplePolicy
    return frozendict(hardcoded_dict)


def main():
    rov_asns_dict = get_real_world_rov_asn_cls_dict()

    # Simulation for the paper
    sim = Simulation(
        percent_adoptions=(
            SpecialPercentAdoptions.ONLY_ONE,
            0.1,
            0.2,
            0.5,
            0.8,
            0.99,
            # Using only 1 AS not adopting causes extreme variance
            # SpecialPercentAdoptions.ALL_BUT_ONE,
        ),
        scenario_configs=(
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                AdoptPolicyCls=PrefixHijackROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
            ),
            ScenarioConfig(
                ScenarioCls=PrefixHijack,
                preprocess_anns_func=preprocess_anns_funcs.origin_hijack,
                AdoptPolicyCls=OriginHijackROV,
                hardcoded_asn_cls_dict=rov_asns_dict,
            )
        ),
        output_dir=Path("~/Desktop/rov_deployment").expanduser(),
        num_trials=20,
        parse_cpus=cpu_count() - 2,
    )
    sim.run()


if __name__ == "__main__":
    main()
