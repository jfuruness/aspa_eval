import time

from .sims import SIMS_TO_RUN, prob_funcs, run_post_rov_motivation_sim


def main():
    """Runs the defaults"""

    for sim in SIMS_TO_RUN:
        start = time.perf_counter()
        sim.run()
        print(f"{time.perf_counter() - start}s for {sim.sim_name}")

    for prob_func in prob_funcs:
        start = time.perf_counter()
        run_post_rov_motivation_sim(prob_func)
        print(f"{time.perf_counter() - start}s for {getattr(sim_func, '__name__', '')}")

if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f"{time.perf_counter() - start}s for all sims")
