"""
Author: tom
Date: 2021-08-31

Usage:
    pairwise_associate.py file [options]

Arguments:
    file=<file>  The file with which to calculate pairwise associations

Options:
    --threshold=<threshold>  The value with which to filter pairwise probabilities
    --ignroe=<ignore>  Column(s) to ignore when considering items in data
"""

import argparse

from pairwise_association.pairwise_associator import PairwiseAssociator


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="""Find pairwise association rules."""
    )

    parser.add_argument(
        "file",
        help="The file with which to calculate pairwise associations",
    )
    parser.add_argument(
        "--threshold",
        help="The value with which to filter pairwise probabilities (default=0.75).",
        required=False,
        default=0.75,
        type=float,
    )
    parser.add_argument(
        "--ignore",
        help="Column(s) to ignore and NOT calculate confidence rules for.",
        required=False,
        action="append",
        default=list(),
    )

    return parser.parse_args()


def pairwise_association():
    args = parse_arguments()
    file = args.file
    threshold = args.threshold
    ignore = args.ignore

    pairwise_associator = PairwiseAssociator(
        file=file,
        threshold=threshold,
        ignore=ignore,
    )
    dataframe = pairwise_associator.load_csv()
    array = pairwise_associator.create_responses_list(dataframe)
    pairwise_associator.create_rules(array)


if __name__ == "__main__":
    pairwise_association()
