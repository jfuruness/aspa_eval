from functools import partial
import time

from .sims import (
    run_origin_hijack_sim,
    run_origin_spoofing_hijack_sim,
    run_shortest_path_export_all_hijack_sim,
    run_shortest_path_export_all_hijack_transit_sim,
    run_route_leak_mh_sim,
    run_route_leak_transit_sim,
)


def main():
    """Runs the defaults"""

    sim_funcs = (
        run_origin_hijack_sim,
        run_origin_spoofing_hijack_sim,
        run_shortest_path_export_all_hijack_sim,
        partial(run_shortest_path_export_all_hijack_sim, num_attackers=10),
        run_route_leak_mh_sim,
        run_route_leak_transit_sim,
        run_shortest_path_export_all_hijack_transit_sim,
    )
    for sim_func in sim_funcs:
        start = time.perf_counter()
        sim_func()  # type: ignore
        print(f"{time.perf_counter() - start}s for {getattr(sim_func, '__name__', '')}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f"{time.perf_counter() - start}s for all sims")
