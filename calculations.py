import math
from scipy.stats import pearsonr, ttest_ind


def amount_n(data: list) -> int:
    return len(data)


def standard_deviation(data: list) -> float:
    sm = 0
    for i in data:
        sm += (i - average(data)) ** 2
    return math.sqrt(sm / (len(data) - 1))


def average(data: list) -> float:
    return sum(data) / len(data)


def minimal(data: list) -> float:
    return min(data)


def maximal(data: list) -> float:
    return max(data)


def deviation(data: list) -> float:
    res = 0
    x = average(data)
    for i in data:
        res += (i - x) ** 2
    return (res / len(data)) ** 0.5


def variation(data: list) -> float:
    return deviation(data) / average(data) * 100


def std_error(data: list) -> float:
    return standard_deviation(data) / math.sqrt(len(data))


def covariance(data_x: list, data_y: list) -> float:
    mean_x = average(data_x)
    mean_y = average(data_y)
    sub_x = [i - mean_x for i in data_x]
    sub_y = [i - mean_y for i in data_y]
    return sum([sub_x[i] * sub_y[i] for i in range(len(sub_x))]) / (len(data_x) - 1)


def pearson(data_x: list, data_y: list) -> float:
    corr_coeff, p_value = pearsonr(data_x, data_y)
    return corr_coeff


def t_test(data_x: list, data_y: list) -> str:
    t_statistic, p_value = ttest_ind(data_x, data_y)
    res = str(t_statistic) + ", " + str(p_value)
    return res

print(t_test([3, 4, 2], [5, 3, 1]))
print(10e+8)