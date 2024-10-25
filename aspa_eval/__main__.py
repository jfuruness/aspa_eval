import time

from .sims import SIMS_TO_RUN


def main():
    """Runs the defaults"""

    for sim in SIMS_TO_RUN:
        start = time.perf_counter()
        sim.run()
        print(f"{time.perf_counter() - start}s for {sim.sim_name}")  # noqa: T201


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    print(f"{time.perf_counter() - start}s for all sims")  # noqa: T201
