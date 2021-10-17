import os
from itertools import permutations
from collections import Counter
from pandas import read_csv, DataFrame

from util.multithread import multithread
from pairwise_associator_enums import ConfThreshold


class PairwiseAssociator:
    def __init__(
        self, file: str, threshold: float = None, ignore: list = list()
    ) -> None:
        self.file = file
        self.threshold = threshold or ConfThreshold.THRESHOLD.value
        self.ignore = ignore

    def load_csv(self) -> DataFrame:
        """Verifies file is provided and valid, extracts relevant headers,
        and loads into dataframe"""
        if (
            not self.file
            or not os.path.exists(self.file)
            or not self.file.endswith(".csv")
        ):
            raise FileNotFoundError
        with open(self.file, "r") as f:
            headers = [
                header.strip()
                for header in f.readline().split(",")
                if header.strip() not in self.ignore
            ]
        df = read_csv(self.file, usecols=headers)
        return df

    @staticmethod
    def _create_qa_pairs(column, dataframe, delimiter=";"):
        """Updates dataframe in place with column name prepended to original values

        Args:
            dataframe (pandas.DataFrame): dataframe with only the data to pair
            delimiter (str): the delimiter within individual values
        """

        dataframe[column] = dataframe[column].apply(
            lambda cell: [f"{column}_{i}" for i in cell.split(delimiter)]
            if delimiter in cell
            else [f"{column}_{cell}"]
        )

    def create_responses_list(self, dataframe):
        """Creates list of all answers with associated question prepended for each row

        Args:
            dataframe (pandas.DataFrame): dataframe from which
                to extract question/answer pairs

        Returns:
            response_list (list): vectorized array of question/answer pairs from the
                passed dataframe
        """
        df = dataframe.copy()
        multithread(
            func=self._create_qa_pairs,
            data_points=df.columns.tolist(),
            dataframe=df,
        )
        response_list = df.sum(axis=1).tolist()
        return response_list

    @staticmethod
    def _update_item_counter(item_list, item_counter):
        """Updates the item_counter Counter with a count of each individual item
            in a larger array

        Args:
            item_list (list): an element of a larger array of items, intended
                to be passed as part of a multithreading function, or at least
                a for loop
            item_counter (Counter): the counter to update
        """
        item_counter.update(item_list)

    @staticmethod
    def _update_pair_counter(item_list, pair_counter):
        """Updates the pair_counter Counter with a count of each pair of items
            in a larger array

        Args:
            item_list (list): an element of a larger array of items, intended
                to be passed as part of a multithreading function, or at least
                a for loop
            pair_counter (Counter): the counter to update
        """
        pair_counter.update(permutations(item_list, 2))

    def _filter_rules_by_conf(self, pair_items, item_counts, rules):
        """Constructs a dictionary of tuple-pairs (a, b), where P(b|a) exceeds the
            provided threshold

        Args:
            pair_counts (collections.Counter): pre-constructed counter
                in which to occurence of pairs of items are stored
            item_counts (collections.Counter): pre-constructed counter
                in which occurence of individual items are stored
            rules (dict): dictionary to store confidence rules in
        """
        conf = pair_items[1] / item_counts.get(pair_items[0][0])
        if conf >= self.threshold:
            rules[pair_items[0]] = conf

    def create_rules(self, array):
        """creates dictionary of rules that meet criteria

        Args:
            array (list): list of lists where each item of each list is
                a tuple-pair of question/response pairs

        Returns:
            rules (dict): a dictionary where each key is a tuple-pair (a, b), and
                each value is the probability of a given b."""
        pair_counts = Counter()
        item_counts = Counter()
        rules = dict()

        multithread(
            func=self._update_item_counter,
            data_points=array,
            item_counter=item_counts,
        )
        multithread(
            func=self._update_pair_counter,
            data_points=array,
            pair_counter=pair_counts,
        )
        multithread(
            func=self._filter_rules_by_conf,
            data_points=pair_counts.items(),
            item_counts=item_counts,
            rules=rules,
        )
        for (a, b) in sorted(rules, key=rules.get, reverse=True):
            print(f"conf({a} => {b}) = {round(rules.get((a, b)), 3)}")
        return rules
