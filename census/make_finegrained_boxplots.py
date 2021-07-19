import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os
from utils import flash_utils
import numpy as np
from data_utils import SUPPORTED_PROPERTIES
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--darkplot', action="store_true",
                        help='Use dark background for plotting results')
    parser.add_argument('--filter', choices=SUPPORTED_PROPERTIES,
                        help='name for subfolder to save/load data from')
    args = parser.parse_args()
    flash_utils(args)

    # Set font size
    plt.rcParams.update({'font.size': 6})

    if args.darkplot:
        # Set dark background
        plt.style.use('dark_background')

    targets = ["0.0", "0.1", "0.2", "0.3", "0.4",
               "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]

    fill_data = np.zeros((len(targets), len(targets)))
    mask = np.ones((len(targets), len(targets)), dtype=bool)
    annot_data = [[None] * len(targets) for _ in range(len(targets))]
    if args.filter == "sex":
        raw_data = [
            [
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [99.95, 99.95, 99.95, 99.95, 100, 99.95, 100, 100, 100, 99.95],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 99.5],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
                [99.95, 99.95, 99.95, 100, 100, 99.95, 99.95, 99.95, 97.85, 99.95]
            ],
            [
                [51.55, 52.55, 51.4, 54.1, 51.9, 52.05, 52.55, 51.55, 52.3, 52.5],
                [61.45, 60.4, 59.1, 58.9, 57.35, 60.9, 59.55, 58.5, 58.85, 59.4],
                [68.0, 64.25, 65.85, 66.8, 67.55, 65.4, 67.1, 66.15, 65.0, 66.0],
                [75.1, 78.23, 71.83, 68.567, 75.73, 75.2, 74.767, 74.467, 67.3, 71.03],
                [77.7, 77.45, 76.15, 73.9, 76.15, 76.65, 77.05, 75.3, 75.55, 78.15],
                [80.85, 78.95, 80.65, 79.65, 79.3, 82.75, 80.75, 67.55, 77.5, 80.4],
                [80.3, 81.75, 75.3, 71.65, 81.0, 78.9, 81.1, 79.5, 83.15, 84.1],
                [78.6, 86.05, 81.15, 82.9, 84.4, 82.3, 87.85, 84.8, 84.75, 85.1],
                [72.05, 72.8, 73.95, 75.7, 70.05, 74.25, 70.3, 65.95, 83.9, 85.2]
            ],
            [
                [52.5, 51.65, 51.2, 50.85, 52.0, 48.7, 52.3, 50.75, 50.05, 49.8],
                [55.7, 57.1, 56.3, 55.9, 57.9, 55.85, 57.3, 58.3, 57.6, 53.9],
                [63.836, 56.7676, 63.2676, 57.567, 50.6764, 59.234, 60.367, 57.13, 56.53, 54.367],
                [63.1, 64.9, 63.5, 64.4, 66.0, 66.25, 65.9, 64.45, 61.6, 65.0],
                [62.35, 64.05, 69.45, 72.95, 65.75, 61.55, 66.25, 61.8, 69.4, 66.55],
                [60.4, 64.3, 70.55, 62.55, 66.1, 61.6, 68.45, 66.6, 64.95, 68.95],
                [72.7, 64.35, 72.2, 73.65, 68.3, 68.95, 68.05, 73.9, 66.8, 71.6],
                [100.0, 98.6, 66.65, 78.05, 80.65, 75.6, 69.95, 100.0, 69.95, 100.0],
            ],
            [
                [51.3, 50.8, 50.75, 49.75, 49.1, 49.95, 50.8, 49.05, 51.15, 49.3],
                [55.067, 52.734, 56.13, 52.5, 50.2, 55.734, 52.7676, 51.03, 52.867, 50.367],
                [58.05, 57.25, 59.2, 59.5, 60.35, 58.35, 60.1, 59.85, 58.6, 59.2],
                [55.45, 55.8, 58.1, 61.75, 63.45, 56.1, 62.75, 65.4, 61.85, 64.75],
                [53.05, 59.45, 66.05, 61.1, 64.5, 57.8, 59.4, 54.05, 57.8, 61.45],
                [64.65, 65.4, 57.1, 70.4, 60.9, 67.75, 65.35, 63.65, 64.95, 64.2],
                [81.4, 69.15, 100.0, 100.0, 69.65, 74.55, 71.25, 77.9, 67.95, 80.85],
            ],
            [
                [47.3, 50.867, 46.1674, 51.2676, 47.13, 49.6, 49.336, 51.467, 47.1, 53.367],
                [51.45, 53.25, 52.95, 53.75, 51.95, 54.3, 54.85, 54.1, 56.05, 53.1],
                [55.75, 56.55, 55.1, 53.95, 51.9, 56.3, 58.15, 53.3, 57.65, 53.45],
                [55.25, 53.95, 54.5, 53.6, 55.05, 53.75, 56.2, 53.7, 56.75, 58.0],
                [61.1, 66.15, 62.75, 58.95, 64.9, 63.65, 60.35, 61.55, 63.2, 58.45],
                [72.4, 67.5, 74.95, 67.5, 67.45, 100.0, 99.95, 100.0, 72.35, 71.65]
            ],
            [
                [52.734, 55.234, 53.53, 52.1, 59.336, 55.2676, 58.0, 57.7, 61.93, 51.43],
                [64.667, 62.567, 61.63, 62.6, 63.7676, 63.93, 64.267, 58.43, 63.7, 63.067],
                [67.73, 68.067, 67.3, 66.9, 66.83, 67.067, 67.367, 67.8, 67.7, 68.2],
                [71.467, 72.1, 70.53, 70.23, 71.0, 70.867, 70.367, 70.934, 70.3, 70.8],
                [82.067, 99.73, 99.0, 81.267, 80.1, 77.867, 78.634, 77.73, 78.8, 82.367]
            ],
            [
                [49.9, 51.1, 50.95, 50.45, 50.25, 50.75, 49.45, 50.3, 51.3, 52.35],
                [52.6, 53.3, 51.6, 53.5, 50.35, 51.05, 54.5, 53.0, 52.25, 52.0],
                [56.2, 55.25, 55.9, 59.95, 55.15, 56.9, 55.65, 55.8, 58.8, 58.1],
                [72.25, 71.4, 69.5, 100.0, 83.6, 100.0, 72.65, 68.75, 66.05, 66.9],
            ],
            [
                [49.65, 52.2, 51.95, 51.6, 50.75, 52.75, 52.65, 52.2, 51.6, 51.1],
                [60.7, 61.35, 59.3, 61.05, 57.05, 58.75, 60.05, 59.0, 56.75, 59.95],
                [68.3, 73.9, 71.95, 66.4, 99.95, 84.1, 72.55, 73.0, 83.8, 66.5]
            ],
            [
                [56.5, 56.35, 55.05, 55.25, 56.7, 55.45, 55.2, 56.3, 55.0, 54.6],
                [87.0, 66.45, 72.5, 79.4, 70.4, 71.95, 100.0, 65.95, 76.3, 72.65]
            ],
            [
                [100.0, 72.9, 73.85, 71.75, 73.2, 72.15, 72.4, 75.95, 66.05, 100.0]
            ]
        ]
    else:
        exit(0)
    
    for i in range(len(targets)):
        for j in range(len(targets)-(i+1)):
            m, s = np.mean(raw_data[i][j]), np.std(raw_data[i][j])
            fill_data[i][j+i+1] = m
            mask[i][j+i+1] = False
            annot_data[i][j+i+1] = r'%d $\pm$ %d' % (m, s)
    
    sns_plot = sns.heatmap(fill_data, xticklabels=targets, yticklabels=targets,
                           annot=annot_data, mask=mask, fmt="^") #, vmin=0, vmax=100)
    sns_plot.set(xlabel= r'$\alpha_0$', ylabel= r'$\alpha_1$')
    sns_plot.figure.savefig("./meta_heatmap_%s.png" % args.filter)
