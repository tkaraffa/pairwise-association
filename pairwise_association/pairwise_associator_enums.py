from enum import Enum


class FakeDataResponses(Enum):

    ONE = "answer_1"
    TWO = "answer_2"
    THREE = "answer_3"
    FOUR = "answer_4"
    # FIVE = "answer_5"
    # SIX = "answer_6"
    # SEVEN = "answer_7"
    # EIGHT = "answer_8"
    # NINE = "answer_9"
    # TEN = "answer_10"


class ConfThreshold(Enum):
    THRESHOLD = 0.75
