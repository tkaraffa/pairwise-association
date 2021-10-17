import os
from itertools import permutations
from collections import defaultdict, Counter
from util.multithread import multithread
from pandas import read_csv
from pairwise_associator_enums import ConfThreshold
from pairwise_associator import PairwiseAssociator
import os
from functools import reduce
import json
from collections import Counter, defaultdict
from pandas import DataFrame
import pytest


from pairwise_associator import PairwiseAssociator


@pytest.fixture(scope="module", autouse=True)
def setup():
    sample_data = DataFrame(
        {
            "test1": ["answer1", "answer1"],
            "test2": ["answer1;answer2", "answer2"],
            "test3": ["answer3", "answer3;answer2"],
        }
    )
    sample_data.to_csv("test_csv.csv", index=False)

    sample_json = {"bad data": ["this", "isn't", "csv"]}
    with open("not-a-csv.json", "w") as f:
        json.dump(sample_json, f)


def teardown():
    for file in ["test_csv.csv", "not-a-csv.json"]:
        os.remove(file)


@pytest.fixture(scope="module", autouse=True)
def cleanup(request):
    request.addfinalizer(teardown)


class TestPairwiseAssociator:

    ## to do
    # add setup task to create file
    # add more tests for rules section of associator

    @pytest.fixture
    def associator(self):
        return PairwiseAssociator("test_csv.csv")

    @pytest.mark.parametrize(
        "file, exception",
        [
            ("test_csv.csv", None),
            (None, FileNotFoundError),
            ("DNE.csv", FileNotFoundError),
            ("not-a-csv.json", FileNotFoundError),
        ],
    )
    def test_load_csv_validity(self, file, exception):
        if exception:
            with pytest.raises(exception):
                PairwiseAssociator(file).load_csv()
        else:
            PairwiseAssociator(file).load_csv()

    @pytest.mark.parametrize(
        "ignore, expected_headers",
        [
            ([], ["test1", "test2", "test3"]),
            (["test1"], ["test2", "test3"]),
            (["test1", "test2", "test3"], []),
        ],
    )
    def test_load_csv_headers(self, ignore, expected_headers):
        associator = PairwiseAssociator("test_csv.csv", ignore=ignore)
        df = associator.load_csv()
        assert df.columns.tolist() == expected_headers

    @pytest.mark.parametrize(
        "column, expected_dataframe",
        [
            (
                "test1",
                DataFrame(
                    {
                        "test1": [["test1_answer1"], ["test1_answer1"]],
                        "test2": [
                            ["test2_answer1", "test2_answer2"],
                            ["test2_answer2"],
                        ],
                        "test3": [
                            ["test3_answer3"],
                            ["test3_answer3", "test3_answer2"],
                        ],
                    }
                ),
            )
        ],
    )
    def test_create_qa_pairs(self, column, expected_dataframe, associator):
        df = associator.load_csv().copy()
        for column in df.columns.tolist():
            associator._create_qa_pairs(column, df)
        assert df.equals(expected_dataframe)
