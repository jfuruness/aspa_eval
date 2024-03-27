import time

from .sims import run_origin_hijack_sim


def main():
    """Runs the defaults"""

    sim_funcs = (run_origin_hijack_sim,)
    for sim_func in sim_funcs:
        start = time.perf_counter()
        sim_func()
        print(f"{time.perf_counter() - start}s for {sim_func.__name__}")


if __name__ == "__main__":
    main()
