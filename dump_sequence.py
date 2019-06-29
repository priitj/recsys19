#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from evaluation import loader

def dump_sequence(data_path, file_prefix, out_fn, density=1, slic=0):
    """
        Convert training/testing slices into a sequence format
        suitable for entropy rate estimation
    """
    #data_path = "data/tmall/slices/"
    #file_prefix = "dataset15"
    #data_path = "data/clef/slices/"
    #file_prefix = "ds"
    #data_path = "data/nowplaying/slices/"
    #file_prefix = "nowplaying"
    #data_path = "data/aotm/slices/"
    #file_prefix = "playlists-aotm"

    #data_path = "data/rsc15/slices/"
    #file_prefix = "rsc15-clicks"
    #data_path = "data/30music/slices/"
    #file_prefix = "30music-200ks"
    #data_path = "data/retailrocket/slices/"
    #file_prefix = "events"

    train, test = loader.load_data(data_path, file_prefix,
        rows_train=None, rows_test=None, density=density,
        slice_num=slic)

    # append all
    all_data = train.append(test)

    # sort by sequence, then timestamp
    groupby = all_data.groupby("SessionId")
    with open(out_fn, "w") as f:
        for session_id, session in groupby:
            item_ids = [item_id for
                item_id in session.sort_values("Time")["ItemId"]]
            for item_id in item_ids:
                f.write("{}\n".format(item_id))
            f.write("-1\n")

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description="Prepare sequence file for entropy rate estimation")
    p.add_argument("-d", type=float, default=1,
        help="downsample the input data (0.1 - use only 10%% of input)")
    p.add_argument("-s", type=int, default=0,
        help="slice number, 0-4")
    p.add_argument("data_path", type=str)
    p.add_argument("file_prefix", type=str)
    p.add_argument("output_file", type=str)
    args = p.parse_args()

    dump_sequence(args.data_path, args.file_prefix, args.output_file,
        args.d, args.s)

