from model_utils import load_model, get_model_folder_path
from data_utils import BoneWrapper, get_df, get_features
import torch.nn as nn
import numpy as np
import utils
from tqdm import tqdm
import os
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 200


def get_models(folder_path, n_models=1000):
    paths = np.random.permutation(os.listdir(folder_path))[:n_models]

    models = []
    for mpath in tqdm(paths):
        model = load_model(os.path.join(folder_path, mpath))
        models.append(model)
    return models


def get_accs(val_loader, models):
    accs = []

    criterion = nn.BCEWithLogitsLoss().cuda()
    for model in tqdm(models):
        model = model.cuda()

        vloss, vacc = utils.validate_epoch(
            val_loader, model, criterion, verbose=False)
        accs.append(vacc)
        # accs.append(vloss)

    return np.array(accs)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=256*32)
    parser.add_argument('--ratio_1', help="ratio for D_1", default="0.5")
    parser.add_argument('--ratio_2', help="ratio for D_2")
    parser.add_argument('--plot', action="store_true")
    args = parser.parse_args()
    utils.flash_utils(args)

    def filter(x): return x["gender"] == 1

    # Ready data
    df_train, df_val = get_df("adv")
    features = get_features("adv")

    # Get data with ratio
    df_1 = utils.heuristic(
        df_val, filter, float(args.ratio_1),
        cwise_sample=10000,
        class_imbalance=1.0, n_tries=300)

    df_2 = utils.heuristic(
        df_val, filter, float(args.ratio_2),
        cwise_sample=10000,
        class_imbalance=1.0, n_tries=300)

    # Prepare data loaders
    ds_1 = BoneWrapper(
        df_1, df_1, features=features)
    ds_2 = BoneWrapper(
        df_2, df_2, features=features)
    loaders = [
        ds_1.get_loaders(args.batch_size, shuffle=False)[1],
        ds_2.get_loaders(args.batch_size, shuffle=False)[1]
    ]

    # Load victim models
    models_victim_1 = get_models(get_model_folder_path("victim", args.ratio_1))
    models_victim_2 = get_models(get_model_folder_path("victim", args.ratio_2))

    # Load adv models
    total_models = 100
    models_1 = get_models(get_model_folder_path(
        "adv", args.ratio_1), total_models // 2)
    models_2 = get_models(get_model_folder_path(
        "adv", args.ratio_2), total_models // 2)

    allaccs_1, allaccs_2 = [], []
    vic_accs, adv_accs = [], []
    for loader in loaders:
        accs_1 = get_accs(loader, models_1)
        accs_2 = get_accs(loader, models_2)

        # # Look at [0, 100]
        accs_1 *= 100
        accs_2 *= 100

        tracc, threshold, rule = utils.find_threshold_acc(accs_1, accs_2)
        print("[Adversary] Threshold based accuracy: %.2f at threshold %.2f" %
              (100 * tracc, threshold))
        adv_accs.append(tracc)

        # Compute accuracies on this data for victim
        accs_victim_1 = get_accs(loader, models_victim_1)
        accs_victim_2 = get_accs(loader, models_victim_2)

        # Look at [0, 100]
        accs_victim_1 *= 100
        accs_victim_2 *= 100

        # Threshold based on adv models
        combined = np.concatenate((accs_victim_1, accs_victim_2))
        classes = np.concatenate(
            (np.zeros_like(accs_victim_1), np.ones_like(accs_victim_2)))
        specific_acc = utils.get_threshold_acc(
            combined, classes, threshold, rule)
        print("[Victim] Accuracy at specified threshold: %.2f" %
              (100 * specific_acc))
        vic_accs.append(specific_acc)

        # Collect all accuracies for basic baseline
        allaccs_1.append(accs_victim_1)
        allaccs_2.append(accs_victim_2)

    adv_accs = np.array(adv_accs)
    vic_accs = np.array(vic_accs)

    # Basic baseline: look at model performance on test sets from both G_b
    # Predict b for whichever b it is higher
    allaccs_1 = np.array(allaccs_1).T
    allaccs_2 = np.array(allaccs_2).T

    preds_1 = (allaccs_1[:, 0] > allaccs_1[:, 1])
    preds_2 = (allaccs_2[:, 0] < allaccs_2[:, 1])
    basic_baseline_acc = (np.mean(preds_1) + np.mean(preds_2)) / 2

    print("[Results] %s v/s %s" % (args.ratio_1, args.ratio_2))
    print("Loss-Test accuracy: %.3f" % (100 * basic_baseline_acc))

    # Threshold baseline: look at model performance on test sets from both G_b
    # and pick the better one
    print("Threshold-Test accuracy: %.3f" %
          (100 * vic_accs[np.argmax(adv_accs)]))

    if args.plot:
        plt.plot(np.arange(len(accs_1)), np.sort(accs_1))
        plt.plot(np.arange(len(accs_2)), np.sort(accs_2))
        plt.savefig("./quick_see.png")
