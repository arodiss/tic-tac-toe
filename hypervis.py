import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import sample
from statistics import median
import warnings


def theil_sen(x, y, order, samples=1000, sample_size=None):
    """Approximation of polynomial Theil-Sen regressor"""
    if order == 0:
        return [np.mean(y)]

    warnings.simplefilter('ignore', np.RankWarning)
    if sample_size is None:
        sample_size = order + 1

    coefficients = []
    for i in range(0, samples):
        sample_indices = sample(range(0, len(x)), sample_size)
        sampled_x = list(x[sample_indices])
        sampled_y = list(y[sample_indices])
        coefficients.append(np.polyfit(sampled_x, sampled_y, order)[0])

    return [median(coefficients)] + \
        theil_sen(
            x,
            y - median(coefficients) * np.power(x, order),
            order-1
        )


data = pd.read_csv('hypersearch.csv')
for param in ['lr_pow', 'pretraining_rounds_1', 'pretraining_rounds_2', 'discount','h1','h2','h3','d1','d2','d3']:
    plt.subplot(1,2,1)
    trend_1 = theil_sen(data[param], data['points'], 1)
    trend_2 = theil_sen(data[param], data['points'], 2)
    predictor_1 = np.poly1d(trend_1)
    predictor_2 = np.poly1d(trend_2)
    x_new = np.linspace(min(data[param]), max(data[param]), 50)
    y_new_1 = predictor_1(x_new)
    y_new_2 = predictor_2(x_new)
    plt.title(param + '-points')
    plt.plot(data[param], data['points'], 'kx')
    plt.plot(x_new, y_new_1, 'b')
    plt.plot(x_new, y_new_2, 'm')

    plt.subplot(1,2,2)
    trend_1 = theil_sen(data[param], data['fatals'], 1)
    trend_2 = theil_sen(data[param], data['fatals'], 2)
    predictor_1 = np.poly1d(trend_1)
    predictor_2 = np.poly1d(trend_2)
    y_new_1 = predictor_1(x_new)
    y_new_2 = predictor_2(x_new)
    plt.title(param + '-fatals')
    plt.plot(data[param], data['fatals'], 'kx')
    plt.plot(x_new, y_new_1, 'b')
    plt.plot(x_new, y_new_2, 'm')

    plt.show()
    plt.close()
