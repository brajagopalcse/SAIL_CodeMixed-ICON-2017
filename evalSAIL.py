#!/usr/bin/env python3

"""
Script to calculate different metrices from the labelled test dataset using the gold dataset for the SAIL (Codemixed) 2017 shared task @ICON-2017.

This script requires the gold annotated file provided by the organizers.

If your system is unable to predict sentiment of a sentence, then tag 'NA' in case of sentiment. 

To run:
python evalSAIL.py gold_dataset.json predicted_dataset.json

This script provides a few metrics. Official score is macro-averaged F-score across all the classes.
"""

import sys, codecs, json
from sklearn import metrics



def get_labels(gold_labels, predicted_labels, class_item):
  gold_class_labels, pred_class_labels = [], []
  for gold, pred in zip(gold_labels, predicted_labels):
    if not gold == class_item:
      continue
    gold_class_labels.append(gold)
    pred_class_labels.append(pred)
  #print(gold_class_labels)
  return gold_class_labels, pred_class_labels


def get_all_labels(gold_file, predicted_file):
  gold_data, predicted_data = [], []
  gold_labels, predicted_labels = [], []
  with codecs.open(gold_file) as f:
    try:
      gold_data = json.load(f)
    except Exception as e:
        print(e)
    f.close()
  with codecs.open(predicted_file) as f:
    try:
      predicted_data = json.load(f)
    except Exception as e:
      print(e)
    f.close()
  
  for gold, pred in zip(gold_data, predicted_data):
    gold_labels.append(gold['sentiment'])
    predicted_labels.append(pred['sentiment'])
  #print(gold_labels, predicted_labels)
  return gold_labels, predicted_labels


if __name__ == '__main__':
  gold_labels, pred_labels = [], []
  if len(sys.argv) < 3 :
    print('Give two input files')
    print('Format should be: python evalSAIL.py gold_dataset.json predicted_dataset.json')
    sys.exit()
  elif len(sys.argv) > 3 :
    print('Input should not be more than two')
    print('Format should be: python evalSAIL.py gold_dataset.json predicted_dataset.json')
    sys.exit()
  else:
    gold_file = sys.argv[1]
    pred_file = sys.argv[2]
    if not gold_file.endswith('.json'):
      print('original file format should be .json')
      sys.exit()
    elif not pred_file.endswith('.json'):
      print('labelled file format should be .json')
      sys.exit()
    else:
      gold_labels, pred_labels = get_all_labels(gold_file, pred_file)

  p = metrics.precision_score(gold_labels, pred_labels, average='macro')
  r = metrics.recall_score(gold_labels, pred_labels, average='macro')
  f = metrics.f1_score(gold_labels, pred_labels, average='macro')
  print('Overall precision = {}, recall = {}, and f-score = {}'.format(p, r, f))

  # for positive sentiment
  gold, predicted = get_labels(gold_labels, pred_labels, 1)
  p = metrics.precision_score(gold, predicted, average='macro')
  r = metrics.recall_score(gold, predicted, average='macro')
  f = metrics.f1_score(gold, predicted, average='macro')
  print('Positive precision = {}, recall = {}, and f-score = {}'.format(p, r, f))

  # for negative sentiment
  gold, predicted = get_labels(gold_labels, pred_labels, -1)
  p = metrics.precision_score(gold, predicted, average='macro')
  r = metrics.recall_score(gold, predicted, average='macro')
  f = metrics.f1_score(gold, predicted, average='macro')
  print('Negative precision = {}, recall = {}, and f-score = {}'.format(p, r, f))
  
  # for neutral sentiment
  gold, predicted = get_labels(gold_labels, pred_labels, 0)
  p = metrics.precision_score(gold, predicted, average='macro')
  r = metrics.recall_score(gold, predicted, average='macro')
  f = metrics.f1_score(gold, predicted, average='macro')
  print('Neural precision = {}, recall = {}, and f-score = {}'.format(p,r,f))

  #print('urgent: \tP R F:\t{:.3f} \t{:.3f} \t{:.3f}'.format(urgentP, urgentR, urgentF))'''

