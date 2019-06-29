#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import time

import numpy as np
from collections import defaultdict

def calc_entropy2(in_fn):
    """
        Entropy rate estimation for a sequence
        input: file with each sequence element (integer) on its own row
    """
    with open(in_fn) as f:
        events = [int(l.strip()) for l in f]

    # calculate Lempel-Ziv estimate of entropy
    lambda_sum = 0
    seq1 = set()                # single item sequences
    seq2 = set()                # two-item sequences
    seq3 = defaultdict(list)    # three-item sequences index

    n = len(events)
    print(in_fn, n)
    timestep = int(n / 10) + 1
    for i in range(n):
        k_max = 0
        # single item
        if events[i] in seq1:
            k_max = 1
            # two items
            if i + 1 < n and tuple(events[i:i+2]) in seq2:
                k_max = 2
                # three or more
                if i + 2 < n:
                    for subseq_start in seq3[tuple(events[i:i+3])]:
                        k = 3
                        while subseq_start + k < i and i + k < n:
                            if events[subseq_start + k] != events[i + k]:
                                break
                            k += 1
                        k_max = max(k, k_max)

        lambda_sum += (k_max + 1) # as in Xu, et al. (2019)
        #print(i, ev, k_max)

        # update index
        seq1.add(events[i])
        if i > 0:
            seq2.add(tuple(events[i-1:i+1]))
            if i > 1:
                 seq3[tuple(events[i-2:i+1])].append(i - 2)

        if i % timestep == 0 and i > 0:
            print(i, "done")

    S = (n / lambda_sum) * np.log2(n)
    print("S:", S)
    print("m (for \Pi^max equation):", len(seq1))

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(
        description="Estimate entropy rate of a sequence of events")
    p.add_argument("input_file", type=str)
    args = p.parse_args()

    calc_entropy2(args.input_file)

