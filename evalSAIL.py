#!/usr/bin/env python3

"""
Script to calculate different metrices from the labelled test dataset using the gold dataset for the SAIL (Codemixed) 2017 shared task @ICON-2017.

This script requires the gold annotated file provided by the organizers.

If your system is unable to predict sentiment of a sentence, then tag 'NA' in case of sentiment. 

To run:
python gold_dataset.json labelled_dataset.json

This script provides a few metrics. Official score is macro-averaged F-score across all the classes.
"""

import sys
from sklearn import metrics

LABELS = ('1', '-1', '0', 'NA')

def load_and_validate(path, constraints=set()):
    """
    Validate list of triage classifications from filename.
    Load into a list of pairs.
    """
    pairs = []
    ids_found = set()

    with open(path) as f:
        for i, line in enumerate(f):
            try:
                idx, label = line.strip().split('\t')
                if label not in LABELS:
                    print('Line {} ({}) in {} has an invalid label, aborting.'\
                            .format(i, line.strip(), path), file=sys.stderr)
                    sys.exit(2)
                if idx in ids_found:
                    print('Duplicate ID on line {} ({}) in {}, aborting.'\
                            .format(i, line.strip(), path), file=sys.stderr)
                    sys.exit(3)
                ids_found.add(idx)
                if constraints and not idx in constraints:
                    print('ID on line {} ({}) in {} is not in CLPsych16 test ids, aborting.'\
                            .format(i, line.strip(), path), file=sys.stderr)
                    sys.exit(4)
                pairs.append((idx, label))
            except ValueError:
                print('Line {} ({}) in {} does not have two columns, aborting.'\
                        .format(i, line.strip(), path), file=sys.stderr)
                sys.exit(1)
    if constraints and len(constraints) != len(ids_found):
        print('Size of test data is incorrect (is {}, should be {}), aborting.'\
                .format(len(ids_found), len(constraints)), file=sys.stderr)
        sys.exit(5)

    pairs.sort(key=lambda x: x[0])

    print('{} validates.'.format(path))

    #print(pairs)

    return pairs


def load_test_ids(path):
    ids = set()
    with open(path) as f:
        for line in f:
            ids.add(line.strip())

    return ids

def make_binary_for_label(pairs, label):

    binary_pairs = []

    for i, (idx, lbl) in enumerate(pairs):
        binary_pairs.append((idx, (lbl == label)))

    return binary_pairs


def make_binary_with_map(pairs, map):

    binary_pairs = []
    for i, (idx, label) in enumerate(pairs):
        binary_pairs.append((idx, map[label]))

    return binary_pairs

def get_labels(pairs):

    labels = []

    for i, (idx, label) in enumerate(pairs):
        labels.append(label)

    return labels


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('test', help='Test file to evaluate.')
    p.add_argument('--gold', help='Gold file to test against. If a gold file \
            is not provided, this script will validate the test file only.')
    p.add_argument('--task', help='Add extra validation checks for a particular task', choices=['clpsych16','clpsych17'])

    args = p.parse_args()

    test_ids = None
    if args.task is not None:
        test_ids = load_test_ids('data/test_ids/{}.tsv'.format(args.task))

    test_pairs = load_and_validate(args.test, test_ids)


    if args.gold:
        gold_pairs = load_and_validate(args.gold)
        if len(test_pairs) != len(gold_pairs):
            print('Number of test and gold instances is not equal, aborting.', file=sys.stderr)
            sys.exit(3)

        print()
        for label in LABELS:
            if label == 'green': continue

            gold = get_labels(make_binary_for_label(gold_pairs, label))
            test = get_labels(make_binary_for_label(test_pairs, label))

            r = metrics.recall_score(gold, test)
            p = metrics.precision_score(gold, test)
            f = metrics.f1_score(gold, test)

            print('{}\tP R F:\t{:.3f} \t{:.3f} \t{:.3f}'.format(label, p, r, f))

        accuracy = metrics.accuracy_score(get_labels(gold_pairs), get_labels(test_pairs));
        macro_f1 = metrics.f1_score(get_labels(gold_pairs), get_labels(test_pairs), average='macro', labels=['crisis', 'red', 'amber'])

        print()
        print("accuracy: {:.3f}".format(accuracy))
        print("macro-averaged f1: {:.3f}".format(macro_f1))
        print()

        flagged_gold = get_labels(make_binary_with_map(gold_pairs, FLAGGED_MAP))
        flagged_test = get_labels(make_binary_with_map(test_pairs, FLAGGED_MAP))

        flaggedP = metrics.precision_score(flagged_gold, flagged_test)
        flaggedR = metrics.recall_score(flagged_gold, flagged_test)
        flaggedF = metrics.f1_score(flagged_gold, flagged_test)

        print('flagged:\tP R F:\t{:.3f} \t{:.3f} \t{:.3f}'.format(flaggedP, flaggedR, flaggedF))

        urgent_gold = get_labels(make_binary_with_map(gold_pairs, URGENT_MAP))
        urgent_test = get_labels(make_binary_with_map(test_pairs, URGENT_MAP))

        urgentP = metrics.precision_score(urgent_gold, urgent_test)
        urgentR = metrics.recall_score(urgent_gold, urgent_test)
        urgentF = metrics.f1_score(urgent_gold, urgent_test)

        print('urgent: \tP R F:\t{:.3f} \t{:.3f} \t{:.3f}'.format(urgentP, urgentR, urgentF))

