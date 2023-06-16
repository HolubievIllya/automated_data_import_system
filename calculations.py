# Імпортуємо модуль math
import math

# Імпортуємо pearsonr, ttest_ind з модулю scipy
from scipy.stats import pearsonr, ttest_ind


def amount_n(data: list) -> int:
    # Повертаємо кількість елементів, тобто довжину списку
    return len(data)


def standard_deviation(data: list) -> float:
    sm = 0
    # Проходить по кожному елементу списку, обчислює квадрат різниці між елементом та середнім значенням списку та підсумовує ці квадрати
    for i in data:
        sm += (i - average(data)) ** 2
    # Потім сума поділяється на (n-1), де n – кількість елементів у списку, і витягується квадратний корінь. Результат заокруглюється до двох знаків після коми
    return round(math.sqrt(sm / (len(data) - 1)), 2)


def average(data: list) -> float:
    # Підсумовує всі елементи списку потім поділяє суму на кількість елементів у списку та округляє результат до двох знаків після коми
    return round(sum(data) / len(data), 2)


def minimal(data: list) -> float:
    # Повертає мінімальне значення
    return min(data)


def maximal(data: list) -> float:
    # Повертає максимальне значення
    return max(data)


def deviation(data: list) -> float:
    res = 0
    # Рахуємо середнє
    x = average(data)
    # Обчислює квадрат різниці між елементом та середнім значенням, підсумовує ці квадрати
    for i in data:
        res += (i - x) ** 2
    # Поділяє суму на кількість елементів у списку. Потім витягується квадратний корінь з отриманого значення, і результат округляється до двох знаків після коми
    return round((res / len(data)) ** 0.5, 2)


def variation(data: list) -> float:
    # Вона ділить середньоквадратичне відхилення на середнє значення списку, потім множить результат на 100 і округляє до двох знаків після коми
    return round(deviation(data) / average(data) * 100, 2)


def std_error(data: list) -> float:
    # Вона ділить стандартне відхилення на квадратний корінь з кількості елементів у списку, і результат округляється до двох знаків після коми за допомогою функції round().
    return round(standard_deviation(data) / math.sqrt(len(data)), 2)


def covariance(data_x: list, data_y: list) -> float:
    # Рахуємо середнє для кожного масиву
    mean_x = average(data_x)
    mean_y = average(data_y)
    # Створює списки, де кожен елемент дорівнює різниці відповідного елемента списку та середнього значення списку
    sub_x = [i - mean_x for i in data_x]
    sub_y = [i - mean_y for i in data_y]
    # Потім відбувається підсумовування cум відповідних елементів і результат ділиться на (n-1), де n - кількість елементів у списку data_x
    return round(
        sum([sub_x[i] * sub_y[i] for i in range(len(sub_x))]) / (len(data_x) - 1), 2
    )


def pearson(data_x: list, data_y: list) -> float:
    corr_coeff = pearsonr(data_x, data_y)
    # Повертає коефіцієнт кореляції та p-значення
    return round(corr_coeff, 2)


def t_test(data_x: list, data_y: list) -> str:
    t_statistic, p_value = ttest_ind(data_x, data_y)
    res = str(round(t_statistic, 2)) + ", " + str(round(p_value, 2))
    # Повертає t-статистику та p-значення для t-тесту незалежних вибірок
    return res
