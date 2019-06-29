# recsys19

These scripts estimate the predictability limits due to randomness and
due to algorithm design in some methods of session-based recommendation.
They can be used to reproduce the results in the Recsys 2019 paper:

P. Järv. *Predictability limits in session-based next item recommen-
dation* RecSys 2019, Copenhagen, Denmark, September 16–20, 2019.

The datasets used come from session-based recommendation evaluation
benchmark, as introduced in:

Ludewig, M., & Jannach, D. (2018). *Evaluation of session-based recommendation algorithms*. User Modeling and User-Adapted Interaction, 28(4-5), 331-390.

## Dependencies

- Python 3
- datasets and scripts from  https://www.dropbox.com/sh/dbzmtq4zhzbj5o9/AACldzQWbw-igKjcPTBI6ZPAa

## Preparation

The benchmark framework is easiest to work with when the the datasets
are extracted under the `data/` subdirectory. Put `entropy.py` and other
scripts in the top level directory of the benchmark framework.

The datasets need to preprocessed into slice files with default settings.

Excerpt from the original instructions:

  1. Unzip any dataset file to the data folder, i.e., rsc15-clicks.dat will then be in the folder data/rsc15/raw
  2. Open the script run_preprocessing\*.py to configure the preprocessing method and parameters
        * run_preprocessing_rsc15.py is for the RecSys challenge dataset.
        * run_preprocessing_tmall.py is for the TMall logs.
        * run_preprocessing_retailrocket.py is for the Retailrocket competition dataset.
        * run_preprocessing_clef.py is for the Plista challenge dataset.
        * run_preprocessing_music.py is for all music datasets (configuration of the input and output path inside the file).
  3. Run the script

## Limit using entropy rate estimation

Convert the session data into a sequence format file:

```
./dump_sequence.py -s 0 data/retailrocket/slices/ events data/retailrocket/seq/s0.txt
```

Entropy rate estimation:

```
./entropy.py data/retailrocket/seq/s0.txt
```

The predictability limit can be computed using the entropy rate estimate
S and the unique event count m that the script outputs.

Multiple slices can be processed at once:

```
for i in 1 2 3 4; do ./dump_sequence.py -s ${i} data/retailrocket/slices/ events data/retailrocket/seq/s${i}.txt; done
for i in 1 2 3 4; do ./entropy.py data/retailrocket/seq/s${i}.txt; done
```


## Limit for some algorithms
