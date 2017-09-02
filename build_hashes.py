import sys
import json
import csv
import pdb
import re
import time
import datetime
import os
import progress_bar
import chinese_japanese_chars as cj

#build_dictionaries
def build_dict(filename):
    """
    pass this method training data and it will create dictionaries, one for the ammount of each negative token,
    one for the amount of each positve token and on probability dictionary which states the probability of each token beeing positive( positive = over 0.5)

    Posiive means that the ticket/token has been solved on the first level of support in this cenario 

    Parameters:
    filename    - Requiered : name of the csv-file with the training data (string)
    """
    dictionary = {}
    regex_noword = re.compile(r"\W", re.IGNORECASE) #everything that is not a word
    regex_digit = re.compile(r"\d", re.IGNORECASE)  #all numbers

    #start processing training data
    csv_file = open(filename, 'r', encoding='utf-8', errors='ignore')
    ticketreader = csv.reader(csv_file, delimiter=',', quotechar='|')
    tickets = list(ticketreader)

    #progress
    l = len(tickets)
    i = 0
    progress_bar.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i, ticket in enumerate(tickets):
        progress_bar.printProgressBar(iteration = i + 1, total = l, prefix = 'Progress:', suffix = 'Complete', length = 50)

        more_tokens = []

        # deleting all the unwanted characters
        line = str(ticket)
        line = line.replace('\\ufeff', ' ') #this is a so called byte order mark (BOM, not relevant anymore)
        line = line.replace(';', ' ')
        line = line.replace(',', ' ')
        line = line.replace('_', ' ')
        line = line.replace('\\n', ' ')
        line = line.replace('\\xa0', ' ')
        line = line.replace('\\t', ' ')
        line = line.replace('\\r', ' ')
        line = line.replace('\\', ' ')
        line = re.sub(regex_noword, ' ', line)
        line = re.sub(regex_digit, ' ', line)
        
        tokens = line.split()
        tokens = list(filter(None, tokens))
        # check for chinese/japanese tokens
        tokens = cj.check_for_cj_chars(tokens)
        
        for token in tokens:
            token = token.lower()
            if token in dictionary:
                dictionary[token] = dictionary[token] + 1
            else:
                dictionary[token] = 1

    csv_file.close()
    return dictionary

"""START OF PROGRAM"""
#type in path to negative training data
print('Please enter the Path to your negative training data')
negative_path = sys.stdin.readline()
negative_path = negative_path.replace('\n', '')

#type in path to positive training data
print('Please enter the Path to your positive training data')
positive_path = sys.stdin.readline()
positive_path = positive_path.replace('\n', '')



#get timestamp begin
timestamp_begin = time.time()

#global declarations
negative_dict = {}   # dictionary list of the amount of each negative token
positive_dict = {}   # dictionary list of the amount of each positive token
probabilities = {}   # dictionary list of each probability of a token
num_in_positives = 0 # amount of a positive token
num_in_negatives = 0 # amount of a negative token

#building the negative dictionary
print('building negative dictionary...')
print('')
negative_dict = build_dict(negative_path)
print('')

# building_positive dictionary
print('building positive dictionary...')    
print('')
positive_dict = build_dict(positive_path)
print('')

#calculate porbabilities
print("calulating probabilities...")
print("iterating through negative_tokens...")
#progress
l = len(negative_dict)
i = 0
progress_bar.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, k in enumerate(negative_dict):
    progress_bar.printProgressBar(iteration = i + 1, total = l, prefix = 'Progress:', suffix = 'Complete', length = 50)
    
    num_in_negatives = negative_dict[k]
    if k in positive_dict:
        num_in_positives = positive_dict[k]
    else:
        num_in_positives = 0

    p = ( num_in_negatives) / ((num_in_negatives ) + (num_in_positives * 2  ))
    if p == 1:
        p = 0.9
        probabilities[k] = p
    else:
        probabilities[k] = p


# calculating the probabilities for the positive_tokens that were not in the negative_token list
print("iterating through positive_tokens...")
l = len(positive_dict)
i = 0
progress_bar.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, k in enumerate(positive_dict):
  progress_bar.printProgressBar(iteration = i + 1, total = l, prefix = 'Progress:', suffix = 'Complete', length = 50)  
  if not (k in negative_dict):
    probabilities[k] = 0.1


# saving the hashes
# saving negatives_dict.csv
print ("saving dictionaries as csv...")
print("saving negatives_dict.json")
try:
    os.remove('negatives_dict.csv')
except FileNotFoundError:
  print("creating negatives_dict.csv....")
  
with open('negatives_dict.csv', 'w', newline='', encoding='utf8') as dict_csv:
    resultwriter = csv.writer(dict_csv, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    resultwriter.writerow(['Token'] + ['Occurences'])
    for token in negative_dict:
      resultwriter.writerow([token] + [negative_dict[token]])
print("finnished saving negatives_dict.json")

#saving positives_dict.csv
print("saving positives_dict.csv")
try:
    os.remove('positives_dict.csv')
except FileNotFoundError:
    print("creating positives_dict.csv....")
    
with open('positives_dict.csv', 'w', newline='', encoding='utf8') as dict_csv:
    resultwriter = csv.writer(dict_csv, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    resultwriter.writerow(['Token'] + ['Occurences'])

    for token in positive_dict:
      resultwriter.writerow([token] + [positive_dict[token]])

print("finnished saving positives_dict.csv")

print("saving probabilities_dict.json")
dict_json = open('probabilities_dict.json', 'w')
dict_json.write(json.dumps(probabilities))
dict_json.close()
print("finnished saving probabilities_dict.json")
print("")

#Information for the user
prob_count = 0
prob_between = 0
prob_0 = 0
prob_1 = 0
prob_gt = 0
prob_lt = 0
prob_5 = 0
for prob in probabilities:
    prob_count = prob_count + 1
    if probabilities[prob] > 0 and probabilities[prob] < 0.9:
        prob_between = prob_between + 1
    if probabilities[prob] == 0.1:
        prob_0 = prob_0 + 1
    if probabilities[prob] == 0.9:
        prob_1 = prob_1 + 1
    if probabilities[prob] > 0.5:
        prob_gt = prob_gt + 1
    if probabilities[prob] < 0.5:
        prob_lt = prob_lt + 1
    if probabilities[prob] == 0.5:
        prob_5 = prob_5 + 1


#get timestamp end / duration
timestamp_end = time.time()
duration = timestamp_end - timestamp_begin

string_total = "program start                 : "
string_total += str(datetime.datetime.fromtimestamp(timestamp_begin).strftime('%Y-%m-%d %H:%M:%S'))
print(string_total)
string_total = "program end                   : "
string_total += str(datetime.datetime.fromtimestamp(timestamp_end).strftime('%Y-%m-%d %H:%M:%S'))
print(string_total)
string_total = "program duration              : "
string_total += str(duration)
string_total += " seconds"
print(string_total)
print("")
string_total = "probabilites total            : "
string_total += str(prob_count)
print(string_total)
string_total = "probabilites between 0 and 0.9: "
string_total += str(prob_between)
print(string_total)
string_total = "probabilites equals 0.1       : "
string_total += str(prob_0)
print(string_total)
string_total = "probabilites equals 0.9       : "
string_total += str(prob_1)
print(string_total)
string_total = "probabilites equals 0.5       : "
string_total += str(prob_5)
print(string_total)
string_total = "probabilites greater than 0.5 : "
string_total += str(prob_gt)
print(string_total)
string_total = "probabilites lesser than 0.5  : "
string_total += str(prob_lt)
print(string_total)
print("")

