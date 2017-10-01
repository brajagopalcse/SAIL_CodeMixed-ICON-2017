#!/usr/bin/env python3

"""
Script to validate the labelled test dataset for the SAIL (Codemixed) 2017 shared task @ICON-2017.

This script requires the original unlabelled file provided by the organizers.

If your system is unable to predict sentiment of a sentence, then tag -2 in case of sentiment. 

To run:
python validateSAIL.py gold.json predicted.json
"""

import sys, codecs, json

sentiment = [0, 1, -1, -2]

def validate(gold_file, pred_file):
  gold_data, pred_data = [], []
  with codecs.open(gold_file) as f:
    try:
      gold_data = json.load(f)
    except Exception as e:
    	print(e)
    f.close()
  with codecs.open(pred_file) as f:
    try:
      pred_data = json.load(f)
    except Exception as e:
      print(e)
    f.close()
  if len(gold_data) > len(pred_data):
    print('There are less items in predicted file')
    sys.exit()
  elif len(gold_data) < len(pred_data):
    print('There are more items in predicted file')
    sys.exit()

  for gold_item, pred_item in zip(gold_data, pred_data):
    gold_id = gold_item['id']
    pred_id = pred_item['id']
    if not gold_id == pred_id:
      print('ID miss match: gold sentence ID = {} and predicted sentence ID = {}'.format(gold_id, pred_id))
      sys.exit()

    gold_text, pred_text = '', ''
    gold_tagged_text, pred_tagged_text = '', ''
    pred_sentiment = ''
    try:
      gold_sent = gold_item['text']
      gold_tagged_sent = gold_item['lang_tagged_text']

      pred_sent = pred_item['text']
      pred_tagged_sent = pred_item['lang_tagged_text']
      pred_sentiment = pred_item['sentiment']
    except Exception as e:
      print(e)
      sys.exit()
    if not gold_sent == pred_sent:
      print('Text miss match at ID = {}'.format(gold_id))
      sys.exit()
    elif not gold_tagged_sent == pred_tagged_sent:
      print('Language tagged text miss match at ID = {}'.format(gold_id))
      sys.exit()
    elif not pred_sentiment in sentiment:
      print('Sentiment tag is different at ID = {}. It should be one of the 0, 1, -1 or -2.'.format(gold_id))
      sys.exit()
  print('Validation Successful. Files are ready to submit.')



if __name__ == '__main__':
  if len(sys.argv) < 3 :
    print('Give two input files')
    print('Format should be: python validateSAIL.py gold.json pred.json')
    sys.exit()
  elif len(sys.argv) > 3 :
    print('Input should not be more than two')
    print('Format should be: python validateSAIL.py gold.json pred.json')
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
      validate(gold_file, pred_file)
