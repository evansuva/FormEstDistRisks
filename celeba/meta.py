import torch as ch
import numpy as np
import os
import argparse
import utils
from data_utils import SUPPORTED_PROPERTIES
from model_utils import get_model_features, BASE_MODELS_DIR


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Celeb-A')
    parser.add_argument('--n_tries', type=int, default=5)
    parser.add_argument('--batch_size', type=int, default=150)
    parser.add_argument('--train_sample', type=int, default=800)
    parser.add_argument('--val_sample', type=int, default=0)
    parser.add_argument('--filter', help='alter ratio for this attribute',
                        default="Male", choices=SUPPORTED_PROPERTIES)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--start_n_conv', type=int, default=0,
                        help="Only consider starting from this layer of conv part")
    parser.add_argument('--first_n_conv', type=int, default=np.inf,
                        help="Only consider first N layers of conv part")
    parser.add_argument('--conv_custom', default=None,
                        help="Comma-separated list of layers wanted (overrides first/last N) for Conv")
    parser.add_argument('--start_n_fc', type=int, default=0,
                        help="Only consider starting from this layer of fc part")
    parser.add_argument('--first_n_fc', type=int, default=np.inf,
                        help="Only consider first N layers of fc part")
    parser.add_argument('--fc_custom', default=None,
                        help="Comma-separated list of layers wanted (overrides first/last N) for FC")
    parser.add_argument('--first', help="Ratio for D_0", default="0.5")
    parser.add_argument('--second', required=True, help="Ratio for D_1")
    parser.add_argument('--focus', choices=["fc", "conv", "all", "combined"],
                        required=True, help="Which layer paramters to use")
    args = parser.parse_args()
    utils.flash_utils(args)

    train_dir_1 = os.path.join(
        BASE_MODELS_DIR, "victim/%s/%s/" % (args.filter, args.first))
    train_dir_2 = os.path.join(
        BASE_MODELS_DIR, "victim/%s/%s/" % (args.filter, args.second))
    test_dir_1 = os.path.join(
        BASE_MODELS_DIR, "adv/%s/%s/" % (args.filter, args.first))
    test_dir_2 = os.path.join(
        BASE_MODELS_DIR, "adv/%s/%s/" % (args.filter, args.second))

    if args.conv_custom is not None:
        args.conv_custom = [int(x) for x in args.conv_custom.split(",")]
    if args.fc_custom is not None:
        args.fc_custom = [int(x) for x in args.fc_custom.split(",")]

    # Load models, convert to features
    dims, vecs_train_1 = get_model_features(
        train_dir_1, first_n_conv=args.first_n_conv,
        start_n_conv=args.start_n_conv,
        start_n_fc=args.start_n_fc,
        conv_custom=args.conv_custom, fc_custom=args.fc_custom,
        first_n_fc=args.first_n_fc, focus=args.focus)
    _, vecs_train_2 = get_model_features(
        train_dir_2, first_n_conv=args.first_n_conv,
        start_n_conv=args.start_n_conv,
        start_n_fc=args.start_n_fc,
        conv_custom=args.conv_custom, fc_custom=args.fc_custom,
        first_n_fc=args.first_n_fc, focus=args.focus)

    _, vecs_test_1 = get_model_features(
        test_dir_1, first_n_conv=args.first_n_conv,
        start_n_conv=args.start_n_conv,
        start_n_fc=args.start_n_fc,
        conv_custom=args.conv_custom, fc_custom=args.fc_custom,
        first_n_fc=args.first_n_fc, focus=args.focus)
    _, vecs_test_2 = get_model_features(
        test_dir_2, first_n_conv=args.first_n_conv,
        start_n_conv=args.start_n_conv,
        start_n_fc=args.start_n_fc,
        conv_custom=args.conv_custom, fc_custom=args.fc_custom,
        first_n_fc=args.first_n_fc, focus=args.focus)

    vecs_train_1 = np.array(vecs_train_1, dtype='object')
    vecs_train_2 = np.array(vecs_train_2, dtype='object')

    Y_test = [0.] * len(vecs_test_1) + [1.] * len(vecs_test_2)
    Y_test = ch.from_numpy(np.array(Y_test)).cuda()
    X_test = vecs_test_1 + vecs_test_2
    X_test = np.array(X_test, dtype='object')

    # Batch layer-wise inputs
    print("Batching data: hold on")
    X_test = utils.prepare_batched_data(X_test)

    accs = []
    for i in range(args.n_tries):

        shuffled_1 = np.random.permutation(len(vecs_train_1))
        vecs_train_1_use = vecs_train_1[shuffled_1[:args.train_sample]]

        shuffled_2 = np.random.permutation(len(vecs_train_2))
        vecs_train_2_use = vecs_train_2[shuffled_2[:args.train_sample]]

        val_data = None
        if args.val_sample > 0:
            vecs_val_1 = vecs_train_1[
                shuffled_1[
                    args.train_sample:args.train_sample+args.val_sample]]
            vecs_val_2 = vecs_train_2[
                shuffled_2[
                    args.train_sample:args.train_sample+args.val_sample]]
            X_val = np.concatenate((vecs_val_1, vecs_val_2))

            Y_val = [0.] * len(vecs_val_1) + [1.] * len(vecs_val_2)
            Y_val = ch.from_numpy(np.array(Y_val)).cuda()
            val_data = (X_val, Y_val)

        # Ready train, test data
        Y_train = [0.] * len(vecs_train_1_use) + [1.] * len(vecs_train_2_use)
        Y_train = ch.from_numpy(np.array(Y_train)).cuda()
        X_train = np.concatenate((vecs_train_1_use, vecs_train_2_use))

        # Batch layer-wise inputs
        print("Batching data: hold on")
        X_train = utils.prepare_batched_data(X_train)

        # Train meta-classifier model
        if args.focus == "all":
            # 795035 params
            dims_conv, dims_fc = dims
            dim_channels, dim_kernels = dims_conv
            metamodel = utils.CombinedPermInvModel(
                dims_fc, dim_channels, dim_kernels)
        elif args.focus == "combined":
            # 827713 params
            dims_conv, dims_fc = dims
            dim_channels, dim_kernels, middle_dim = dims_conv
            metamodel = utils.FullPermInvModel(
                dims_fc, middle_dim, dim_channels, dim_kernels,)
        elif args.focus == "conv":
            # 590225 params
            dim_channels, dim_kernels = dims
            metamodel = utils.PermInvConvModel(dim_channels, dim_kernels)
        else:
            # 204721 params
            metamodel = utils.PermInvModel(dims)

        print("Total parameters:", utils.get_param_count(metamodel))

        metamodel = metamodel.cuda()

        # Train PIM model
        _, test_acc = utils.train_meta_model(
            metamodel,
            (X_train, Y_train),
            (X_test, Y_test),
            epochs=args.epochs, binary=True,
            lr=0.001, batch_size=args.batch_size,
            val_data=val_data, combined=True,
            eval_every=10, gpu=True)
        accs.append(test_acc)
        print("Run %d: %.2f" % (i+1, test_acc))

    print(accs)
