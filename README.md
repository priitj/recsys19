# recsys19

These scripts estimate the predictability limits due to randomness and
due to algorithm design in some methods of session-based recommendation.
They can be used to reproduce the results in the Recsys 2019 paper:

P. Järv. *Predictability limits in session-based next item recommendation* RecSys 2019, Copenhagen, Denmark, September 16–20, 2019.

The datasets used come from session-based recommendation evaluation
benchmark, as introduced in:

Ludewig, M., & Jannach, D. (2018). *Evaluation of session-based recommendation algorithms*. User Modeling and User-Adapted Interaction, 28(4-5), 331-390.

## Dependencies

- Python 3
- datasets and source code from  https://www.dropbox.com/sh/dbzmtq4zhzbj5o9/AACldzQWbw-igKjcPTBI6ZPAa

## Preparation

To reproduce the experiments, the datasets need to be preprocessed into 5-way testing and training splits. Use the scripts that come with the session-based recommendation evaluation benchmark and datasets.

Get the files in this repository:

```
git clone https://github.com/priitj/recsys19.git
```

Download the source code of the session-based benchmark suite. Folders hosted on Dropbox can be downloaded as ZIP files by browsing into the folder and selecting "Download -> Direct download" from the menu.

Extract it in the directory where we cloned this repository.

```
cd recsys19
unzip Source-Code.zip
```

This will also create an empty `data/` directory which will be used to hold the raw and preprocessed data. Download datasets and extract them under this folder, for example:

```
cd data
unzip nowplaying.zip
```

As a result, there should be a file `nowplaying.csv` in the directory `data/nowplaying/raw/`. Edit the preprocessing scripts and change the `METHOD` variable to "slice" and the PATH_PROCESSED variable to point to the `slices` subdirectory under the dataset, for example `data/nowplaying/slices/`. Other options should be left as default.

Preprocessing scripts (excerpt from the original instructions):

* run_preprocessing_rsc15.py is for the RecSys challenge dataset.
* run_preprocessing_tmall.py is for the TMall logs.
* run_preprocessing_retailrocket.py is for the Retailrocket competition dataset.
* run_preprocessing_clef.py is for the Plista challenge dataset.
* run_preprocessing_music.py is for all music datasets (configuration of the input and output path inside the file).

Run the preprocessing scripts for the datasets downloaded.

## Limit using entropy rate estimation

Convert the session data into a sequence format file:

```
./dump_sequence.py -s 0 data/retailrocket/slices/ events data/retailrocket/seq/s0.txt
```

Entropy rate estimation:

```
./entropy.py data/retailrocket/seq/s0.txt
```

Multiple slices can be processed at once:

```
for i in 1 2 3 4; do ./dump_sequence.py -s ${i} data/retailrocket/slices/ events data/retailrocket/seq/s${i}.txt; done
for i in 1 2 3 4; do ./entropy.py data/retailrocket/seq/s${i}.txt; done
```

The predictability limit can be computed using the entropy rate estimate
S and the unique event count m.

The MATLAB script `predictability.m` computes the Pi^max value for a single
sample and `pred_limits.m` over multiple datasets and slices (for that, put S
results in a tab-separated file `entropy.tsv` and m values in `count.tsv`. Both
files require a header row with dataset names).

## Limit for some algorithms

Calculate co-occurrence of the item to predict (in a recommendation
accuracy test) and the current item (given to the recommender as an input)
in the training data.

```
./find_limits.py  data/retailrocket/slices/ events
```

`"r_cnt"` in results is the total number of test cases examined.

Interpreting the results:

| Key        | Item to predict appears | Applies to algorithm  |
| ------------- | ------------- | ----- |
| cnt_next      | next to current item | MC, SF-SKNN |
| cnt_fwd10     | among 10 items after current item | SR |
| cnt_anywhere  | anywhere in session | AR, IKNN |
| cnt_anywhere_sess | in session with any current session item | \*SKNN |


