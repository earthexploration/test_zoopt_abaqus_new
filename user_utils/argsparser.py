import argparse

def argsparser():
    # Experiment setting
    parser = argparse.ArgumentParser("zoopt search")
    parser.add_argument("--budget", default=4, type=int)
    return parser.parse_known_args()[0].__dict__