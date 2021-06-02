import argparse
import datetime as dt
import logging
import os
import sys
from functools import cmp_to_key

import traverse_states as ts
import states


# Directory where logs are written to
_const_log_directory = "./log/"


def parse_arguments(raw_args):
    """
    Sets up the argument parser, parses the arguments.
    :return: the parsed args
    """
    # TODO Create description for project and enter it here
    parser = argparse.ArgumentParser(description='state_ranker')

    # what level to log at
    logging_level_group = parser.add_mutually_exclusive_group()
    logging_level_group.set_defaults(verbosity=logging.WARNING)
    logging_level_group.add_argument('-d', '--debug',
        action='store_const', const=logging.DEBUG, dest='verbosity',
        help='log debug messages')
    logging_level_group.add_argument('-v', '--verbose',
        action='store_const', const=logging.INFO, dest='verbosity',
        help='log informational messages')
    logging_level_group.add_argument('-q', '--quiet',
        action='store_const', const=logging.ERROR, dest='verbosity',
        help='only log errors')

    # should log arguments be written to the console
    parser.add_argument('-c', '--console',
        action='store_true', help='display log output on the console')

    return parser.parse_args(args=raw_args)


def verify_arguments(parsed_args):
    """
    Verifies that passed-in arguments are all valid.
    If an argument is invalid, this may either print a warning
        indicating the issue and the value it will use instead, or it
        may fail the execution
    """
    logging.info("Verifying project arguments")
    logging.info(parsed_args)

    # TODO verify any arguments here that need verification


def init_logging(logging_level=logging.WARNING, to_std_out=True):
    """
    Initializes logging, by default prints to std out.
    Note that the logging levels are: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    :param logging_level: The level of logging to log at
    :param to_std_out: Whether to print to standard out, in addition to the default log file name
    :return: The root logger
    """
    root = logging.getLogger()
    root.setLevel(logging_level)

    formatter_string = '%(asctime)s [%(levelname)s] %(message)s'
    formatter = logging.Formatter(formatter_string)

    # Set up logging to a log file of the name yyyy-mm-dd-hh-mm-ss.log
    now_time = dt.datetime.now()

    log_directory = _const_log_directory
    if not os.path.isdir(log_directory):
        os.makedirs(log_directory)

    log_extension = '.log'
    log_file_path = os.path.join(log_directory,
                                 str(now_time.year).zfill(4) + "-" +
                                 str(now_time.month).zfill(2) + "-" +
                                 str(now_time.day).zfill(2) + "_" +
                                 str(now_time.hour).zfill(2) + "-" +
                                 str(now_time.minute).zfill(2) + "-" +
                                 str(now_time.second).zfill(2) +
                                 log_extension)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(formatter)
    root.addHandler(file_handler)

    # Set up logging to stdout if requested in the parameters
    if to_std_out:
        std_out_handler = logging.StreamHandler(sys.stdout)
        std_out_handler.setLevel(logging_level)
        std_out_handler.setFormatter(formatter)
        root.addHandler(std_out_handler)

    return root, log_file_path


def compute_pop(combos):
    pops = []
    for combo in combos:
        state_combo = combo.split('-')
        logging.debug(f"state_combo({state_combo})")
        running_pop = 0
        running_gdp = 0
        for state in state_combo:
            running_pop += states.attributes[state]["pop"]
            running_gdp += states.attributes[state]["gdp"]
        pops.append((combo, running_pop, running_gdp))
    return pops


def pop_comparator(item1, item2):
    return item2[1] - item1[1]

def sort_by_pop(pops):
    return sorted(pops, key=cmp_to_key(pop_comparator))

def main(raw_args):
    parsed_args = parse_arguments(raw_args)
    root, path = init_logging(logging_level=parsed_args.verbosity, to_std_out=parsed_args.console)
    logging.info(f"Logging initialized with\n\tverbosity: {parsed_args.verbosity}\n\tfilepath: {path}\n\twriting to console: {parsed_args.console}")
    verify_arguments(parsed_args)
    state_combos = ts.traverse(states.adjacencies, 4)
    logging.debug(f"state_combos({state_combos})")
    pops = compute_pop(state_combos)
    logging.debug(f"pops({pops})")
    sorted_combos = sort_by_pop(pops)

    for i, sorted_combo in enumerate(sorted_combos):
        print(f"{sorted_combo}")

if __name__ == "__main__":
    main(sys.argv[1:])
