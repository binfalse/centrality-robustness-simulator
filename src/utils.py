from datetime import datetime
import time
import math


MAX_EXP_PROBABILITY = 1.0e250


def get_time() -> str:
    """
    get a useful time string
    """
    return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


def degree_probability_lin(x: int) -> float:
    """
    function to scale the probability of a node *linearly* according to it's degree

    :param x: the node's degree
    :return: the scaled value
    """
    return x


def degree_probability_exp(x: int) -> float:
    """
    function to scale the probability of a node *exponentially* according to it's degree

    :param x: the node's degree
    :return: the scaled value
    """
    try:
        return min(math.exp(x), MAX_EXP_PROBABILITY)
    except:
        return MAX_EXP_PROBABILITY


def degree_probability_log(x: int) -> float:
    """
    function to scale the probability of a node *logarithmically* according to it's degree

    :param x: the node's degree
    :return: the scaled value
    """
    return math.log(x + 1)


class StopClock:
    def __init__(self):
        self.start = time.time()
        self.end = 0
        self.last = 0

    def get_duration(self) -> float:
        return self.end - self.start

    def stop(self) -> str:
        self.end = time.time()
        s = "took "
        if self.last > 0:
            s += f"{self.end - self.last} s ({self.end - self.start} s in total)"
        else:
            s += f"{self.end - self.start} s"

        self.last = self.end
        return s
