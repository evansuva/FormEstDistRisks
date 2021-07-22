import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--darkplot', action="store_true",
                        help='Use dark background for plotting results')
    parser.add_argument('--legend', action="store_true",
                        help='Add legend to plots')
    parser.add_argument('--novtitle', action="store_true",
                        help='Remove Y-axis label')
    args = parser.parse_args()

    first_cat = " 0.5"

    if args.darkplot:
        # Set dark background style
        plt.style.use('dark_background')

    # Set font size
    # plt.rcParams.update({'font.size': 18})
    plt.rcParams.update({'font.size': 14})

    data = []
    columns = [
        r'Female proportion of training data ($\alpha$)',
        "Accuracy (%)",
        r'$n$'
    ]

    categories = ["0.2", "0.3", "0.4", "0.6", "0.7", "0.8"]
    raw_data = {
        "3 (all)": {
            10: [
                    [49.35, 54.1, 50.05, 53.9, 88.3, 56.95, 50.65, 54.5, 50.75, 59.95],
                    [85.9, 55.7, 53.7, 54.0, 51.45, 50.8, 62.2, 49.45, 52.9, 52.8],
                    [49.95, 51.0, 49.8, 50.2, 49.65, 50.65, 50.35, 51.35, 50.95, 49.35],
                    [59.6, 48.95, 52.9, 48.3, 51.75, 50.8, 49.1, 48.85, 47.85, 49.3],
                    [50.45, 53.05, 50.05, 50.7, 55.4, 50.65, 49.95, 59.9, 49.8, 48.8],
                    [51.15, 67.4, 55.85, 50.4, 54.1, 58.8, 51.25, 58.25, 53.9, 65.55]
                ],
            20: [
                    [51.45, 48.05, 50.8, 48.65, 53.1, 52.8, 56.5, 49.35, 61.75, 61.6],
                    [51.9, 53.7, 64.35, 60.55, 67.65, 53.15, 50.65, 53.1, 54.55, 50.0],
                    [50.75, 49.9, 49.55, 50.35, 49.95, 48.85, 50.15, 49.25, 59.3, 48.4],
                    [49.35, 49.3, 50.9, 51.55, 49.9, 50.3, 49.7, 52.1, 50.95, 50.95],
                    [50.85, 64.05, 54.95, 91.85, 88.15, 48.85, 49.1, 52.85, 50.2, 84.05],
                    [62.7, 87.95, 60.25, 50.4, 51.15, 99.3, 54.0, 51.75, 59.05, 93.95]
                ],
            40: [
                    [61.1, 81.25, 79.05, 50.45, 86.0, 51.05, 50.8, 73.55, 51.0, 63.95],
                    [50.95, 51.75, 51.8, 51.35, 49.75, 50.8, 56.2, 84.35, 93.2, 87.4],
                    [51.35, 62.35, 48.6, 52.9, 51.7, 56.7, 51.95, 60.2, 52.95, 51.35],
                    [50.95, 50.3, 51.5, 51.25, 56.05, 50.5, 49.15, 51.0, 55.4, 51.25],
                    [69.75, 79.7, 51.8, 84.55, 70.2, 59.95, 51.4, 76.8, 51.25, 87.9],
                    [67.7, 69.05, 96.55, 83.4, 95.4, 96.05, 80.1, 97.45, 84.25, 99.7]
                ],
            1600: [
                    [99.55, 99.7, 99.7, 99.55, 99.9, 99.95, 99.7, 98.05, 99.95, 99.8],
                    [94.7, 95.7, 93.45, 92.4, 95.35, 97.25, 96.6, 94.25, 95.9, 98.0],
                    [70.95, 63.85, 63.25, 69.75, 59.2, 66.3, 74.6, 63.4, 69.45, 65.55],
                    [50.0, 58.9, 61.55, 67.0, 58.55, 62.15, 59.85, 58.75, 62.65, 65.65],
                    [70.2, 90.3, 75.7, 83.75, 86.0, 89.45, 85.1, 83.7, 78.35, 72.35],
                    [99.45, 99.2, 98.75, 98.4, 97.1, 92.05, 96.0, 96.75, 96.6, 97.35]
                ]
        },
        "1": {
            10: [
                    [98.75, 98.05, 69.55, 49.4, 98.95, 85.85, 50.05, 98.7, 51.0, 99.15],
                    [74.5, 82.0, 84.3, 75.7, 84.95, 85.5, 50.35, 82.7, 85.0, 69.2],
                    [50.15, 58.95, 54.15, 58.6, 50.0, 62.35, 56.35, 66.6, 56.25, 67.7],
                    [63.65, 62.65, 66.35, 72.25, 57.9, 56.25, 65.1, 51.7, 71.6, 55.0],
                    [76.9, 94.5, 60.6, 50.0, 55.95, 84.9, 97.5, 71.2, 98.15, 75.8],
                    [97.95, 98.3, 98.0, 99.3, 84.8, 98.05, 98.25, 99.65, 83.7, 95.6]
                ],
            20: [
                    [99.3, 99.45, 99.05, 97.1, 94.15, 50.0, 96.8, 97.4, 98.95, 94.15],
                    [90.35, 54.2, 51.6, 90.25, 58.15, 84.75, 70.1, 68.95, 91.9, 82.45],
                    [51.05, 55.8, 68.15, 50.15, 62.85, 59.6, 54.45, 63.45, 60.85, 70.0],
                    [50.95, 70.45, 53.25, 50.0, 69.8, 56.15, 61.7, 50.9, 64.45, 51.55],
                    [50.0, 80.7, 50.25, 83.15, 80.75, 68.1, 90.7, 98.75, 61.75, 77.65],
                    [95.2, 91.4, 50.35, 99.85, 96.85, 99.95, 69.2, 97.85, 69.75, 99.95]
                ],
            40: [
                    [98.2, 99.15, 99.8, 50.0, 98.95, 48.9, 48.35, 99.2, 95.4, 99.45],
                    [81.75, 77.05, 49.8, 98.0, 92.7, 51.3, 69.55, 88.6, 96.55, 86.25],
                    [61.6, 79.6, 50.8, 78.05, 65.1, 57.5, 50.15, 69.8, 57.4, 53.2],
                    [63.75, 51.0, 55.7, 57.8, 57.95, 64.6, 53.55, 55.15, 62.6, 74.6],
                    [90.4, 94.1, 96.95, 87.0, 70.65, 90.35, 89.35, 68.85, 61.15, 89.7],
                    [61.95, 98.65, 51.0, 95.7, 99.35, 97.65, 98.3, 92.25, 97.3, 93.15]
                ],
            1600: [
                    [98.95, 99.7, 99.5, 99.65, 99.8, 99.8, 99.55, 99.75, 50.0, 99.85],
                    [93.15, 56.35, 91.5, 93.1, 93.7, 93.55, 87.3, 93.2, 90.85, 95.95],
                    [79.2, 73.15, 79.8, 54.65, 70.75, 64.9, 68.5, 67.35, 60.95, 50.0],
                    [67.15, 58.8, 54.2, 55.7, 59.7, 63.0, 71.8, 50.0, 55.45, 61.0],
                    [82.45, 84.5, 98.85, 79.95, 81.3, 74.5, 80.3, 80.55, 80.8, 74.0],
                    [98.4, 99.25, 98.25, 97.95, 98.55, 91.0, 97.4, 96.95, 98.85, 99.5]
                ]
        }
    }

    focus_n = 1600
    for n, v1 in raw_data.items():
        v2 = v1[focus_n]
        for i in range(len(v2)):
            for j in range(len(v2[i])):
                data.append([categories[i], v2[i][j], n])

    df = pd.DataFrame(data, columns=columns)
    sns_plot = sns.boxplot(x=columns[0], y=columns[1], hue=columns[2],
                           data=df, showfliers=False)

    if args.novtitle:
        plt.ylabel("", labelpad=0)

    # Accuracy range, with space to show good performance
    sns_plot.set(ylim=(45, 101))

    # Add dividing line in centre
    lower, upper = plt.gca().get_xlim()
    midpoint = (lower + upper) / 2
    plt.axvline(x=midpoint, color='white' if args.darkplot else 'black',
                linewidth=1.0, linestyle='--')

    # Map range to numbers to be plotted
    targets_scaled = range(int((upper - lower)))
    # plt.plot(targets_scaled, baselines, color='C1', marker='x', linestyle='--')

    if not args.legend:
        plt.legend([],[], frameon=False)

    # Make sure axis label not cut off
    plt.tight_layout()

    sns_plot.figure.savefig("./meta_boxplot_varying_n.png")
