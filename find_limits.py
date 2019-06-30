#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from evaluation import loader
from collections import defaultdict

def test_all(data_path, file_prefix, density=1, slic=[0]):
    #data_path = 'data/tmall/slices/'
    #file_prefix = 'dataset15'
    #data_path = 'data/clef/slices/'
    #file_prefix = 'ds'
    #data_path = 'data/rsc15/slices/'
    #file_prefix = 'rsc15-clicks'
    #data_path = 'data/nowplaying/slices/'
    #file_prefix = 'nowplaying'
    #data_path = 'data/aotm/slices/'
    #file_prefix = 'playlists-aotm'
    #data_path = 'data/30music/slices/'
    #file_prefix = '30music-200ks'
    #data_path = 'data/retailrocket/slices/'
    #file_prefix = 'events'

    all_stats = defaultdict(int)
    for i in slic:
        train, test = loader.load_data(data_path, file_prefix,
            rows_train=None, rows_test=None, density=density,
            slice_num=i)

        s, i2s = load_sessions(train)
        print(data_path, file_prefix, i)

        stats = test_reachability(s, i2s, test)
        for k, v in stats.items():
            all_stats[k] += v
    for k, v in all_stats.items():
        print(k, v)

def test_reachability(sessions, item2session, data, max_span=10):
    """Item co-occurrence in sessions"""
    stats = {"r_cnt" : 0,
        "cnt_next" : 0,
        "cnt_fwd10" : 0,
        "cnt_anywhere" : 0,
        "cnt_anywhere_sess" : 0}

    groupby = data.groupby("SessionId")
    for session_id, session in groupby:
        item_ids = [item_id for
            item_id in session.sort_values("Time")["ItemId"]]

        l = len(item_ids)
        for i in range(l - 1):
            # step 1: calculate relative to current item
            # MC cnt_next
            # SR, windowed NB cnt_fwd10
            # AR cnt_anywhere
            item_id = item_ids[i]
            target_id = item_ids[i + 1]

            next_found = 0
            fwd10_found = 0
            any_found = 0
            sess_found = 0
            seen_sessions = set()

            # loop through all sessions
            for train_sess_id in item2session[item_id]:
                seen_sessions.add(train_sess_id)
                train_sess = sessions[train_sess_id]
                last_item = None
                for i, train_item in enumerate(train_sess):
                    if train_item == target_id:
                        any_found = 1
                        sess_found = 1
                        if last_item == item_id:
                            next_found = 1
                            fwd10_found = 1
                            break
                        elif not fwd10_found and i > 1 and item_id in train_sess[max(0, i - max_span):i - 1]:
                            fwd10_found = 1
                    last_item = train_item

                if next_found:
                    break
                # otherwise need to keep searching other sessions

            # step 2: search using the remainder of the items seen so far
            # NB cnt_anywhere_sess
            if not sess_found:
                sess_so_far = set(item_ids[:i])
                for item_id in sess_so_far:
                    for train_sess_id in item2session[item_id]:
                        if train_sess_id in seen_sessions:
                            continue
                        seen_sessions.add(train_sess_id)

                        train_sess = sessions[train_sess_id]
                        last_item = None
                        for i, train_item in enumerate(train_sess):
                            if train_item == target_id:
                                sess_found = 1
                                break

            # summarize results
            stats["r_cnt"] += 1
            stats["cnt_next"] += next_found
            stats["cnt_fwd10"] += fwd10_found
            stats["cnt_anywhere"] += any_found
            stats["cnt_anywhere_sess"] += sess_found

    return stats

def test_forward_backward(sessions, item2session, data):
    """Statistics of whether the item to predict occurs
    before or after the current item (when co-occurring in a session)
    """
    stats = {"f_cnt" : 0,
        "cnt_bwd" : 0,
        "cnt_fwd" : 0,
        "cnt_both" : 0}

    groupby = data.groupby("SessionId")
    for session_id, session in groupby:
        item_ids = [item_id for
            item_id in session.sort_values("Time")["ItemId"]]

        l = len(item_ids)
        for i in range(l - 1):
            item_id = item_ids[i]
            target_id = item_ids[i + 1]
            if item_id == target_id:
                continue

            common_sessions = set(item2session[item_id]).intersection(
                set(item2session[target_id]))

            bwd = 0
            fwd = 0
            both = 0

            # loop through all sessions
            for train_sess_id in common_sessions:
                train_sess = sessions[train_sess_id]
                item_pos = []
                target_pos = []
                for i in range(len(train_sess)):
                    if train_sess[i] == item_id:
                        item_pos.append(i)
                    elif train_sess[i] == target_id:
                        target_pos.append(i)

                b = f = 0
                if min(target_pos) < max(item_pos):
                    b = 1
                if min(item_pos) < max(target_pos):
                    f = 1
                bwd += b
                fwd += f
                if b == f:
                    both += 1

            # summarize results
            stats["f_cnt"] += len(common_sessions)
            stats["cnt_bwd"] += bwd
            stats["cnt_fwd"] += fwd
            stats["cnt_both"] += both

    return stats

def test_out_edges(sessions, item2session):
    """Count outgoing edges in an item-to-item graph
       (edge is one item following another in a session)
    """
    stats = {"e_cnt" : 0,
        "cnt_u20" : 0,
        "cnt_u10" : 0,
        "cnt_u05" : 0}

    out_cnt = defaultdict(set)
    for session_id, item_ids in sessions.items():

        last_item_id = None
        for item_id in item_ids:
            if last_item_id is not None:
                out_cnt[last_item_id].add(item_id)
            last_item_id = item_id

    for item_id, out_edges in out_cnt.items():
        stats["e_cnt"] += 1
        l = len(out_edges)
        if l <= 20:
            stats["cnt_u20"] += 1
            if l <= 10:
                stats["cnt_u10"] += 1
                if l <= 5:
                    stats["cnt_u05"] += 1

    return stats

def load_sessions(data):
    """Build a dictionary of sessions and a lookup map for
    finding which sessions an item belongs to
    """
    sessions = defaultdict(list)
    item2session = defaultdict(list)

    groupby = data.groupby("SessionId")
    for session_id, session in groupby:
        item_ids = [item_id for
            item_id in session.sort_values("Time")["ItemId"]]
        sessions[session_id] = item_ids

        for item_id in item_ids:
            item2session[item_id].append(session_id)

    return sessions, item2session

if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser(
        description="Calculate accuracy limits for some algorithms")
    p.add_argument("-d", type=float, default=1,
        help="downsample the input data (0.1 - use only 10%% of input)")
    p.add_argument("data_path", type=str)
    p.add_argument("file_prefix", type=str)
    args = p.parse_args()

    test_all(args.data_path, args.file_prefix, args.d, [0,1,2,3,4])

