import time

from .sims import SIMS_TO_RUN, prob_funcs, run_post_rov_motivation_sim


def main():
    """Runs the defaults"""

    for sim in SIMS_TO_RUN:
        start = time.perf_counter()
        sim.run()
        print(f"{time.perf_counter() - start}s for {sim.sim_name}")  # noqa: T201

    for prob_func in prob_funcs:
        start = time.perf_counter()
        run_post_rov_motivation_sim(prob_func)
        print(  # noqa: T201
            f"{time.perf_counter() - start}s for {getattr(prob_func, '__name__', '')}"
        )


if __name__ == "__main__":
    print("47m for 100 trials using 100 CPUs")
    print("278m (~4.6hrs) for 100 trials using 100 CPUs")
    start = time.perf_counter()
    main()
    print(f"{time.perf_counter() - start}s for all sims")  # noqa: T201
