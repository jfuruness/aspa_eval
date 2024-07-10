from functools import partial
import time

from .sims import (
    run_forged_origin_export_all_hijack_sim,  # noqa
    run_forged_origin_export_all_hijack_transit_sim,  # noqa
    run_neighbor_spoofing_hijack_sim,  # noqa
    run_shortest_path_export_all_hijack_sim,  # noqa
    run_forged_origin_hijack_adoption_scenarios_sim,  # noqa
    run_shortest_path_export_all_hijack_input_clique_sim,  # noqa
    run_shortest_path_export_all_hijack_etc_sim,  # noqa
    run_shortest_path_export_all_hijack_etc_cc_sim,  # noqa
    run_route_leak_mh_sim,  # noqa
    run_route_leak_transit_sim,  # noqa
    run_post_rov_motivation_sim,  # noqa
    prob_funcs,  # noqa
    run_shortest_path_export_all_hijack_etc_cc_w_bgp_sim,
)


def main():
    """Runs the defaults"""

    sim_funcs = [
        run_forged_origin_hijack_adoption_scenarios_sim,
        run_forged_origin_export_all_hijack_transit_sim,
        run_shortest_path_export_all_hijack_etc_cc_w_bgp_sim,
        run_neighbor_spoofing_hijack_sim,
        run_forged_origin_export_all_hijack_sim,
        run_shortest_path_export_all_hijack_sim,
        partial(run_shortest_path_export_all_hijack_sim, num_attackers=10),
        run_route_leak_mh_sim,
        run_route_leak_transit_sim,
        run_shortest_path_export_all_hijack_input_clique_sim,
        run_shortest_path_export_all_hijack_etc_sim,
        run_shortest_path_export_all_hijack_etc_cc_sim,
    ]
    for prob_func in prob_funcs:
        post_rov_func = partial(run_post_rov_motivation_sim, prob_func)
        post_rov_func.__name__ = prob_func.__name__  # type: ignore
        sim_funcs.append(post_rov_func)

    for sim_func in sim_funcs:
        start = time.perf_counter()
        sim_func()  # type: ignore
        print(f"{time.perf_counter() - start}s for {getattr(sim_func, '__name__', '')}")


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f"{time.perf_counter() - start}s for all sims")
