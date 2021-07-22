import seaborn as sns
import matplotlib.pyplot as plt
import argparse
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
    parser.add_argument('--mode', choices=["meta", "threshold"],
                        default="meta",
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
        raw_data_threshold = [
            [
                [78.5, 74.8, 74.35, 78.75, 76.8],
                [89.2, 88.75, 88.5, 85.75, 88.6],
                [91.9, 92.65, 91.7, 90.4, 92.65],
                [91.2, 90.35, 92, 85.1, 90.65],
                [64.05, 61.60, 63.45, 63.60, 59.00, 61.65, 64.35, 63.35, 62.25, 63.55],
                [84.8, 82, 84, 87.05, 85.5],
                [90.85, 89.5, 91.35, 90.3, 91.4],
                [94.1, 92.9, 93.35, 93.85, 93.85],
                [94.5, 93.3, 93.05, 94.55, 94.7],
                [98.05, 98.05, 94.6, 98.1, 98.1]
            ],
            [
                [55.6, 54.65, 53.55, 54.2, 54.2],
                [50.8, 56.85, 56.5, 52.15, 57.1],
                [50.95, 54.2, 53.55, 55.75, 53.95],
                [55.35, 60.35, 65.00, 59.65, 61.20, 54.35, 60.90, 56.70, 60.55, 57.60],
                [83.35, 81, 82.2, 80.9, 81.75],
                [92.5, 92.65, 93.3, 91, 92.55],
                [95.75, 95, 94.9, 94.65, 94.5],
                [95.65, 95.75, 94.15, 96.3, 96.15],
                [58.3, 58.65, 98.35, 56.65, 60.3]
            ],
            [
                [50.85, 50.85, 50.9, 50, 52.9],
                [59.3, 55.5, 58.2, 56.4, 57.65],
                [65.45, 62.85, 55.05, 61.35, 59.15, 60.00, 59.40, 66.25, 60.90, 61.40],
                [81.85, 83.65, 81.95, 84.55, 83.85],
                [93.25, 93.65, 93.05, 93.05, 80.06],
                [95.75, 95.45, 95.9, 96.05, 95.2],
                [96.6, 95.75, 71.7, 96.05, 95.85],
                [98.85, 62.75, 64.55, 99.2, 98.85],
            ],
            [
                [55.4, 57.2, 56.05, 55.35, 57.7],
                [60.95, 67.40, 61.25, 64.10, 66.60, 58.00, 62.40, 64.60, 62.60, 66.00],
                [82.5, 82.1, 81.6, 82, 83.5],
                [92.75, 92.75, 91.65, 91.45, 92.75],
                [92.2, 94.85, 94.75, 95.35, 94],
                [95.25, 95.2, 94.9, 94.65, 95.45],
                [98.45, 66.1, 97.45, 98.7, 68.15]
            ],
            [
                [61.85, 59.10, 54.95, 56.65, 60.55, 61.95, 60.80, 61.20, 61.75, 59.90],
                [73.65, 72.35, 76.2, 73.35, 76.1],
                [89.1, 87.5, 88, 88.7, 88.1],
                [89.65, 92.25, 90.4, 90.85, 92.05],
                [90.85, 91.6, 92.4, 91.15, 19.95],
                [95.65, 91.95, 90.8, 89.9, 91.95]
            ],
            [
                [64.05, 63.65, 63.90, 62.35, 64.20, 62.90, 64.15, 61.50, 62.85, 63.15],
                [68.35, 76.40, 69.65, 74.05, 76.30, 76.20, 74.85, 75.30, 75.80, 75.90],
                [76.65, 77.90, 77.15, 74.05, 78.50, 74.90, 80.55, 82.80, 74.10, 74.00],
                [70.80, 71.55, 70.25, 68.50, 70.30, 65.45, 70.15, 70.45, 66.00, 71.35],
                [60.30, 62.20, 61.30, 53.80, 57.15, 62.75, 62.50, 62.00, 60.40, 61.85],
            ],
            [
                [67.4, 65, 65.25, 64.15, 63.3],
                [73.95, 73.2, 68.5, 74.7, 73.95],
                [64, 70.6, 70.25, 70.95, 69.4],
                [86.25, 86.35, 83.45, 84.45, 79.8]
            ],
            [
                [57.15, 56.45, 55.5, 57.2, 55.05],
                [55.3, 51.1, 52.9, 50.75, 51.9],
                [69.75, 65, 58.55, 57, 72.6]
            ],
            [
                [55.2, 51.05, 56.2, 56.7, 56.45],
                [61.85, 63.1, 59.45, 63.7, 62.6],
            ],
            [
                [57.3, 60.35, 50.1, 54.2, 55.75]
            ]
        ]
    else:
        exit(0)

    if args.mode == "meta":
        data_use = raw_data
    else:
        data_use = raw_data_threshold 


    for i in range(len(targets)):
        for j in range(len(targets)-(i+1)):
            m, s = np.mean(data_use[i][j]), np.std(data_use[i][j])
            fill_data[i][j+i+1] = m
            mask[i][j+i+1] = False
            annot_data[i][j+i+1] = r'%d $\pm$ %d' % (m, s)

    sns_plot = sns.heatmap(fill_data, xticklabels=targets, yticklabels=targets,
                           annot=annot_data, mask=mask,
                           fmt="^", vmin=50, vmax=100)
    sns_plot.set(xlabel=r'$\alpha_0$', ylabel=r'$\alpha_1$')
    sns_plot.figure.savefig("./meta_heatmap_%s_%s.png" % 
                            (args.filter, args.mode))
