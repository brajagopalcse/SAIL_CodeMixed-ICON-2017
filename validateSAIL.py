#!/usr/bin/env python3

"""
Script to validate the labelled test dataset for the SAIL (Codemixed) 2017 shared task @ICON-2017.

This script requires the original unlabelled file provided by the organizers.

If your system is unable to predict sentiment of a sentence, then tag 'NA' in case of sentiment. 

To run:
python original_unlablled_dataset.json labelled_dataset.json
"""

import sys, codecs, json

sentiment = [0, 1, -1]

def validate(original_file, labelled_file):
  original_data, labelled_data = [], []
  with codecs.open(original_file) as f:
    try:
      original_data = json.load(f)
    except error:
      print(error)
    f.close()
  with codecs.open(labelled_file) as f:
    try:
      labelled_data = json.load(f)
    except error:
      print(error)
    f.close()
  if len(original_data) > len(labelled_data):
    print('There are less items in labelled data')
    sys.exit()
  elif len(original_data) < len(labelled_data):
    print('There are more items in labelled data')
    sys.exit()
  for i in range(len(original_data)):
    orginal_sentence = original_data[i]
    labelled_sentence = labelled_data[i]
    original_id = orginal_sentence['id']
    labelled_id = labelled_sentence['id']
    if not original_id == labelled_id:
      print('ID miss match: original ID = {} and labelled ID = {}'.format(original_id, labelled_id))
      sys.exit()
    elif not orginal_sentence['text'] == labelled_sentence['text']:
      print('Text miss match at ID = {}'.format(original_id))
      sys.exit()
    elif not original_sentence['lang_tagged_text'] == labelled_sentence['lang_tagged_text']:
      print('Language tagged text miss match at ID = {}'.format(original_id))
      sys.exit()
    elif not labelled_sentence['sentiment'] in sentiment:
      if not labelled_sentence['sentiment'] == 'NA':
        print('Sentiment tag is different at ID = {}. It should be one of the 0, 1, -1 or NA.'.format(original_id))



if __name__ == '__main__':
  if len(sys.argv) < 3 :
    print('Give two input files')
    print('Format should be: python original_unlablled_test.json labelled_test.json')
    sys.exit()
  elif len(sys.argv) > 3 :
    print('Input should not be more than two')
    print('Format should be: python original_unlablled_test.json labelled_test.json')
    sys.exit()
  else:
    original_file = sys.argv[1]
    labelled_file = sys.argv[2]
    if(not original_file.endswith('.json')):
      print('original file format should be .json')
      sys.exit()
    elif(not labelled_file.endswith('.json')):
      print('labelled file format should be .json')
      sys.exit()
    else:
      validate(original_file, labelled_file)
