import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from utils import flash_utils
from data_utils import SUPPORTED_PROPERTIES
import numpy as np
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--darkplot', action="store_true",
                        help='Use dark background for plotting results')
    parser.add_argument('--filter', choices=SUPPORTED_PROPERTIES,
                        default="Male",
                        help='name for subfolder to save/load data from')
    parser.add_argument('--mode', choices=["meta", "threshold"],
                        default="meta")
    args = parser.parse_args()
    flash_utils(args)

    # Set font size
    plt.rcParams.update({'font.size': 6})
    plt.rc('xtick', labelsize=9)
    plt.rc('ytick', labelsize=9)
    plt.rc('axes', labelsize=10)

    if args.darkplot:
        # Set dark background
        plt.style.use('dark_background')

    targets = ["0.0", "0.1", "0.2", "0.3", "0.4",
               "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]

    fill_data = np.zeros((len(targets), len(targets)))
    mask = np.ones((len(targets), len(targets)), dtype=bool)
    annot_data = [[None] * len(targets) for _ in range(len(targets))]
    if args.filter == "Male":
        raw_data_meta = [
            [
                [50.87, 55.82, 54.62, 54.92, 50.32],
                [64.25, 60.23, 53.1, 63.63, 65.03],
                [74.01, 77.71, 54.57, 72.16, 65.57],
                [86.52, 77.79, 88.41, 84.89, 71.06],
                [92.81, 91.56, 88.87, 84.37, 80.72],
                [88.17, 94.79, 92.44, 91.66, 92.03],
                [77.71, 96.55, 91.75, 96.85, 96.95],
                [86.29, 94.91, 96.06, 91.54, 93.43],
                [98.05, 97.10, 92.70, 95.60, 97.15],
                [93.70, 95.55, 91.90, 84.91, 98.21]
            ],
            [
                [52.17, 51.28, 53.68, 46.76, 49.83],
                [59.85, 56.4, 60.15, 57.5, 52.45],
                [74.62, 71.09, 62.46, 72.63, 58.89],
                [78.86, 72.76, 74.51, 75.81, 86.81],
                [89.68, 87.59, 85.24, 88.42, 84.98],
                [87.5, 90.6, 93.25, 94.2, 89.85],
                [96.38, 98.03, 97.21, 94.17, 89.32],
                [98.0, 94.75, 92.6, 97.3, 94.15],
                [95.55, 95.8, 92.3, 90.65, 98.15]
            ],
            [
                [52.62, 56.36, 55.36, 54.74, 48.72],
                [60.17, 58.4, 59.66, 56.91, 59.37],
                [55.38, 66.10, 70.38, 57.28, 68.88],
                [67.49, 72.4, 75.73, 81.75, 80.64],
                [69.14, 78.29, 80.75, 89.34, 91.96],
                [93.46, 94.65, 94.15, 91.67, 85.93],
                [90.96, 86.5, 87.83, 93.92, 91.91],
                [97.99, 91.57, 93.86, 88.84, 88.17]
            ],
            [
                [48.93, 52.96, 51.33, 53.06, 53.88],
                [56.42, 56.72, 56.52, 57.57, 53.42],
                [72.16, 64.65, 69.45, 64.44, 74.19],
                [74.0, 72.75, 75.25, 77.2, 81.15],
                [93.59, 85.20, 91.78, 78.47, 84.06],
                [92.6, 93.15, 95.55, 91.9, 89.25],
                [95.95, 94.2, 96.4, 93.35, 91.95]
            ],
            [
                [51.15, 48.75, 49.97, 51.45, 52.58],
                [55.76, 59.11, 60.82, 61.14, 57.41],
                [59.70, 65.58, 68.69, 58.89, 65.37],
                [69.53, 83.06, 81.70, 88.51, 83.57],
                [89.43, 85.04, 77.53, 79.21, 88.36],
                [93.41, 91.73, 96.48, 91.88, 87.9]
            ],
            [
                [53.88, 47.84, 52.16, 49.92, 54.56],
                [63.17, 64.27, 56.12, 51.67, 58.77],
                [77.01, 82.18, 81.77, 73.15, 73.32],
                [84.16, 81.46, 80.01, 78.41, 82.36],
                [80.1, 92.45, 93.65, 85.26, 89.26]
            ],
            [
                [48.49, 47.86, 50.63, 50.89, 51.67],
                [33.30, 77.27, 72.16, 68.72, 49.12],
                [75.5, 70.86, 72.47, 72.31, 69.4],
                [80.60, 68.14, 63.87, 64.18, 59.75],
            ],
            [
                [66.56, 37.83, 64.50, 48.32, 48.72],
                [68.6, 69.7, 50.3, 52.65, 51.25],
                [79.35, 56.7, 75.0, 79.6, 66.95]
            ],
            [
                [45.60, 71.41, 54.31, 60.15, 41.08],
                [50.12, 55.46, 62.37, 42.07, 76.66]
            ],
            [
                [56.25, 46.95, 47.4, 56.0, 56.15]
            ]
        ]

        raw_data_threshold = [
            [
                [50.68, 50.03, 51.24],
                [53.89, 54.91, 52.67],
                [55.56, 52.84, 55.20],
                [56.25, 57.01, 61.31],
                [54.2, 56.9, 58.05],
                [59.09, 60.98, 61.03],
                [67.37, 61.94, 63.95],
                [72, 71.8, 71.95],
                [76.65, 76.49, 75.68],
                [76.1, 76.4, 74.8]
            ],
            [
                [51.23, 51.08, 51.49],
                [50.36, 51.98, 52.74],
                [53.83, 51.43, 53.67],
                [50.48, 55.57, 53.66],
                [58.63, 59.97, 57.71],
                [66.79, 59.99, 64.71],
                [69.74, 66.77, 68.13],
                [74.50, 73.43, 71.79],
                [73.58, 75.59, 75.79]
            ],
            [
                [51.54, 50.82, 51.28],
                [51.13, 51.34, 51.96],
                [51.63, 51.77, 52.57],
                [58.04, 57.28, 58.56],
                [61.72, 62.69, 63.46],
                [69.67, 70.03, 70.48],
                [72.87, 73.44, 72.46],
                [76.03, 75.32, 76.64]
            ],
            [
                [50.15, 50.92, 50.61],
                [52.09, 53.34, 52.44],
                [54.05, 56.76, 55.17],
                [59, 63.2, 62],
                [68.18, 64.66, 64.3],
                [67.65, 66.89, 71.57],
                [73.71, 71.54, 73.91]
            ],
            [
                [51.14, 52.05, 50.97],
                [56.34, 52.89, 56.91],
                [61.34, 58.24, 61.24],
                [61.76, 65.81, 68.34],
                [71.91, 65.71, 67.5],
                [68.64, 74.05, 73.04]
            ],
            [
                [55.68, 55.41, 51.96],
                [60.68, 60.43, 60.18],
                [62.3, 60.9, 63.05],
                [66.26, 68.39, 67.63],
                [72.45, 72.4, 69.05]
            ],
            [
                [53.79, 55.99, 56.3],
                [55.83, 60.32, 60.57],
                [62.1, 65.05, 59.94],
                [66.43, 69.59, 67.19]
            ],
            [
                [53.54, 55, 51.68],
                [58.64, 55.63, 57.52],
                [59.23, 62.75, 56.66]
            ],
            [
                [51.72, 53.04, 51.77],
                [57.6, 54.85, 57.8]
            ],
            [
                [54.86, 54.51, 53.7]
            ]
        ]

        raw_data_loss = [
            [53.12, 53.15, 52.13, 51.44, 51.15, 52.92, 50.86, 50.5, 51.74, 50.4],
            [51.09, 52.01, 51.59, 50.53, 50.14, 50.6, 48.91, 52.63, 50.19],
            [52.34, 50.46, 50.34, 50.83, 50.19, 50.84, 50.41, 50.14],
            [50.06, 50.01, 54.65, 51.06, 50.05, 50.32, 49.64],
            [50.44, 56.9, 51.91, 53.84, 52.43, 50.19],
            [50.78, 57.26, 56.9, 46.62, 50.1],
            [52.19, 58.1, 51.53, 48.62],
            [52.06, 50.1, 49.85],
            [55.03, 45.95],
            [50.42]
        ]

    elif args.filter == "Young":

        raw_data_meta = [
            [
                [50.74, 54.47, 52.7],
                [60.06, 50.29, 49.71],
                [63.23, 63.5, 61.17],
                [66.17, 61.62, 68.26, 63.23, 63.49, 61.17],
                [80.05, 74.6, 79.2, 76.95, 78.15],
                [81.62, 81.62, 81.72],
                [84.55, 82.37, 80.6],
                [85.13, 86.66, 86.53],
                [83.31, 87.15, 81.32],
                [85.6, 87.26, 83.6]
            ],
            [
                [51.42, 50.95, 51.03],
                [55.64, 57.78, 50.68],
                [50.23, 63.84, 61.76],
                [71.05, 70.77, 68.85, 70.87, 71.59],
                [76.43, 74.58, 73.84],
                [75.31, 80.04, 77.81],
                [48.92, 80.57, 81.85],
                [84.08, 86.87, 82.28],
                [87.5, 86.73, 50.01]
            ],
            [
                [52.12, 50.01, 52.14],
                [56.75, 49.2, 49.86],
                [62.27, 61.41, 64.04, 60.55, 51.06],
                [64.93, 67.63, 60.48],
                [67.82, 73.86, 73.81],
                [74.8, 73.6, 74.96],
                [74.2, 76.55, 80.52],
                [82.94, 80.25, 80.22]
            ],
            [
                [49.35, 50.26, 49.19],
                [51.07, 54.46, 48.93, 53.03, 53.65],
                [58.72, 59.67, 59.40],
                [62.25, 65.91, 65.39],
                [66.39, 69.06, 68.6],
                [74.06, 71.77, 70.46],
                [75.78, 51.03, 76.46]
            ],
            [
                [52.95, 52.67, 51.64, 50.03, 49.44],
                [50.12, 54.47, 54.85],
                [57.56, 59.77, 59.67],
                [50.85, 50.86, 64.26],
                [70.73, 67.01, 67.98],
                [75.47, 69.2, 75.39]
            ],
            [
                [51.65, 51.24, 51.37, 51.27, 51.52],
                [54.24, 54.04, 53.32, 53.35, 54.37],
                [58.94, 51.11, 58.21, 48.89, 58.26],
                [64.08, 62.8, 64.86, 63.58, 64.15],
                [69.26, 69.82, 72.60, 71.3, 73.09]
            ],
            [
                [51.71, 50.17, 51.37],
                [53.24, 49.03, 53.01],
                [60.99, 50.94, 57.17],
                [65.4, 65.38, 66.14]
            ],
            [
                [51.38, 50.54, 50.93],
                [53.46, 55.68, 48.99],
                [62.86, 62.55, 62.45]
            ],
            [
                [52.05, 50.72, 50.91],
                [57.47, 57.55, 58.05]
            ],
            [
                [51.36, 51.67, 48.93]
            ]
        ]
        raw_data_threshold = [
            [
                [49.77, 49.72, 50.28],
                [48.37, 54.76, 48.27],
                [50.25, 50.35, 50.25],
                [48.32, 50.3, 50.25],
                [50.27, 50.28, 50.28],
                [49.07, 49.02, 48.92],
                [50.03, 50.03, 50.41],
                [39.52, 49.52, 49.52],
                [76.06, 50.33, 50.23],
                [50.48, 88.89, 50.63]
            ],
            [
                [47.94, 52.1, 52.06],
                [49.98, 49.98, 49.98],
                [50.65, 49.75, 42.7],
                [49.95, 50, 49.95],
                [48.13, 52.07, 48.08],
                [49.15, 49.55, 49.65],
                [49.14, 49.19, 49.14],
                [58.83, 49.85, 67.85],
                [80.5, 75.35, 80.3]
            ],
            [
                [52.03, 52.03, 47.97],
                [52.06, 48.52, 52.0],
                [51.95, 48, 52.06],
                [49.79, 55.81, 50.16],
                [55.31, 51.28, 50.97],
                [51.24, 52.79, 55.37],
                [53.12, 60.78, 58.07],
                [70.8, 66.06, 56.33]
            ],
            [
                [50.03, 49.1, 48.9],
                [49.93, 49.88, 49.78],
                [51.33, 47.13, 41.48],
                [50.63, 51.03, 50.33],
                [49.16, 49.21, 51.04],
                [52.43, 54.41, 55.14],
                [56.08, 50.03, 64.18]
            ],
            [
                [51.4, 50.05, 53.35],
                [55.75, 60.92, 61.59],
                [65.76, 71.35, 60.99],
                [61.74, 67.38, 68.24],
                [72.02, 74.52, 83.25],
                [90.85, 90.8, 83.2]
            ],
            [
                [51.15, 48.65, 51.87],
                [50.90, 50.7, 52.06],
                [55.34, 51.17, 51.78],
                [51.91, 51.96, 50.60],
                [53.35, 59.55, 54.2],
            ],
            [
                [52.9, 52.49, 49.36],
                [57.36, 56.01, 54.29],
                [51.62, 58.08, 55.88],
                [67.32, 70.99, 60.05]
            ],
            [
                [51.02, 51.12, 50.92],
                [53.42, 50.50, 50.6],
                [52.41, 54.02, 52.41]
            ],
            [
                [49.54, 49.38, 49.38],
                [49.29, 49.24, 49.39]
            ],
            [
                [50.1, 49.85, 49.85]
            ]
        ]

        raw_data_loss = [
            [52.56, 56.11, 61.73, 59.91, 57.7, 83.25, 84.07, 81.94, 85.51, 98.4],
            [52.56, 55.37, 50.6, 55.97, 79.34, 88.53, 83.97, 81.04, 96.67],
            [51.89, 47.61, 59.95, 64.5, 79.35, 75.67, 85.25, 93.88],
            [50.51, 51.55, 53.56, 67.96, 66.36, 84.08, 90.47],
            [52.08, 62.8, 77.01, 70.3, 85.99, 95.85],
            [47.83, 50.13, 71.48, 62.82, 86.9],
            [57.09, 66.22, 73.07, 88.55],
            [55.68, 58.78, 85.23],
            [50.03, 73.89],
            [63.5]
        ]
    else:
        raise ValueError("Unknown filter: {}".format(args.filter))

    # TODO: Rearrange data according to 1 - ratio

    if args.mode == "meta":
        for i in range(len(targets)):
            for j in range(len(targets)-(i+1)):
                m, s = np.mean(raw_data_meta[i][j]), np.std(raw_data_meta[i][j])
                fill_data[i][j+i+1] = m
                mask[i][j+i+1] = False
                annot_data[i][j+i+1] = r'%d $\pm$ %d' % (m, s)

        sns_plot = sns.heatmap(fill_data, xticklabels=targets,
                               yticklabels=targets, annot=annot_data,
                               mask=mask, fmt="^")

    else:
        for i in range(len(targets)):
            for j in range(len(targets)-(i+1)):
                m, s = np.mean(raw_data_threshold[i][j]), np.std(
                    raw_data_threshold[i][j])
                fill_data[j+i+1][i] = m
                mask[j+i+1][i] = False
                annot_data[j+i+1][i] = r'%d $\pm$ %d' % (m, s)

        for i in range(len(targets)):
            for j in range(len(targets)-(i+1)):
                m = raw_data_loss[i][j]
                fill_data[i][j+i+1] = m
                mask[i][j+i+1] = False
                annot_data[i][j+i+1] = r'%d' % m

        for i in range(len(targets)):
            fill_data[i][i] = 0
            mask[i][i] = False
            annot_data[i][i] = "N.A."

        sns_plot = sns.heatmap(fill_data, xticklabels=targets,
                               yticklabels=targets, annot=annot_data,
                               mask=mask, fmt="^",
                               vmin=50, vmax=100)

    sns_plot.set(xlabel=r'$\alpha_0$', ylabel=r'$\alpha_1$')
    sns_plot.figure.savefig("./meta_heatmap_%s_%s.png" % (args.filter, args.mode))
