import pdb
import sys
import json
import csv
import re
import time
import datetime
import os
import progress_bar
import chinese_japanese_chars as cj

#sort probabilities which have the most "distance" to 0.5
def sort_func(x):
  return abs(token_probs[x] - 0.5)

"""START OF PROGRAM"""
#type in path to tickets
print('Please enter the Path to the tickets you want to check')
ticket_path = sys.stdin.readline()
ticket_path = ticket_path.replace('\n', '')

#get timestamp
timestamp_begin = time.time()

#global declarations
result = {}                                       #list of the final result (ticket-number and probability)
probabilities = {}                                #list for the porbability dictionary
tickets = {}                                      #list for all the imported tickets             
regex_notdigit = re.compile(r"\D", re.IGNORECASE) # RegEx will find everything that is not a digit
regex_noword = re.compile(r"\W", re.IGNORECASE)   # RegEx will find only chars that are not a word, or word-character
regex_digit = re.compile(r"\d", re.IGNORECASE)    # RegEx will find everything that is digits
total_prob = 0                                    #all calculated probabilities
unknown_probs = 0                                 #all probabilities that were not in the training sets
no_prob = 0                                       #all probabilities that could not be calculated
final_prob_0 = 0                                  #all probabilities that are 0 
final_prob_1 = 0                                  #all probabilities that are 1
final_prob_5 = 0                                  #all probabilities that are 0.5
final_prob_gt = 0                                 #all probabilities that are greater than 0.5
final_prob_lt = 0                                 #all probabilities that are lower than 0.5 

#get probabilites
print("opening probabilities_dict.json...")
file = open('probabilities_dict.json', 'r', encoding='utf-8' )
json_probs = file.read()
probabilities = json.loads(json_probs)
file.close()
print("finished openening probabilities_dict.json...")

#get tickets / prepare tickets
print("preparing tickets...")
with open(ticket_path, newline='', encoding='utf8') as csvfile:
  ticketreader = csv.reader(csvfile, delimiter=',', quotechar='|')
  for i, row in enumerate(ticketreader):
    if i == 0: 
      continue

    ticket = str(row)
    ticket_split = ticket.split(',', 1)
    #get ticket number
    ticket_no = ticket_split[0]
    ticket_no = ticket_no.replace('\\ufeff', '') #this is a so called byte order mark (BOM, not relevant anymore)
    ticket_no = re.sub(regex_notdigit, '', ticket_no)

    #get ticket body without ticket number
    ticket_body = ticket_split[1]

    ticket_body = ticket_body.replace(';', ' ')
    ticket_body = ticket_body.replace(',', ' ')
    ticket_body = ticket_body.replace('_', ' ')
    ticket_dody = ticket_body.replace('\\ufeff', '') #this is a so called byte order mark (BOM, not relevant anymore)
    ticket_body = ticket_body.replace('\\n', ' ')
    ticket_body = ticket_body.replace('\\xa0', ' ')
    ticket_body = ticket_body.replace('\xa0', ' ')
    ticket_body = ticket_body.replace('\\t', ' ')
    ticket_body = ticket_body.replace('\\r', ' ')
    ticket_body = ticket_body.replace('\\', ' ')
    ticket_body= re.sub(regex_noword, ' ', ticket_body)
    ticket_body = re.sub(regex_digit, ' ', ticket_body)
    
    tickets[ticket_no] = ticket_body

print("finished preparing tickets...")

# calculation of the probabilites
print("calculating probabilities...")
#progress
l = len(tickets)
i = 0
progress_bar.printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
for i, ticket in enumerate(tickets):
  progress_bar.printProgressBar(iteration = i + 1, total = l, prefix = 'Progress:', suffix = 'Complete', length = 50)
  
  more_tokens = [] # additional tokens if the current token is a string of chinese/japanese characters  
  token_probs = {} # array of the probabilities which occour in the current ticket
  
  tokens = tickets[ticket].split()

# check for chinese/japanese tokens
  tokens = cj.check_for_cj_chars(tokens)
      
  for token in tokens:     
    token = token.lower()
    if token in probabilities:
      token_probs[token] = probabilities[token]
    else:
      unknown_probs = unknown_probs + 1
      token_probs[token] = 0.5


  # sort token probabilities by distance from .5
  # and pull out the top X ones to use to calculate total probability
  max_tokens = 15
  interesting_tokens = []
  c=0
  for w in sorted(token_probs, key=sort_func, reverse=True):
    interesting_tokens.append(token_probs[w])
    if c >= max_tokens:
      break
    c = c+1

  # calculate real probabilitiy
  a = 1
  b = 1
  for token in interesting_tokens:
    a = a * token
    b = b * ( 1 - token )
     
  if a + b == 0:
    result[ticket_no] = 'no probabilites determined'
    no_prob = no_prob + 1
  else:
    final_prob = a / ( a + b )
    result[ticket] = final_prob
    total_prob = total_prob + 1
    if final_prob == 0.1:
      final_prob_0 = final_prob_0 + 1
    if final_prob == 0.9:
      final_prob = final_prob_1 + 1
    if final_prob == 0.5:
      final_prob_5 = final_prob_5 + 1
    if final_prob > 0.5:
      final_prob_gt = final_prob_gt + 1
    if final_prob < 0.5:
      final_prob_lt = final_prob_lt + 1

    
print("finished calculating probabilities")

#write result.csv
print("saving result.csv")
try:
    os.remove('result.csv')
except FileNotFoundError:
  print("creating result.csv....")
with open('result.csv', 'w', newline='') as csvfile:
    resultwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    resultwriter.writerow(['Ticket'] + ['Probability'])
    for ticket in result:
      resultwriter.writerow([ticket] + [result[ticket]])
    
print("finnished saving result.csv")

#get timestamp end / duration
timestamp_end = time.time()
duration = timestamp_end - timestamp_begin

#print Programm Information
print("")
print("Program Duration Info:")
string_total = "program start   : "
string_total += str(datetime.datetime.fromtimestamp(timestamp_begin).strftime('%Y-%m-%d %H:%M:%S'))
print(string_total)
string_total = "program end     : "
string_total += str(datetime.datetime.fromtimestamp(timestamp_end).strftime('%Y-%m-%d %H:%M:%S'))
print(string_total)
string_total = "program duration: "
string_total += str(duration)
string_total += " seconds"
print(string_total)

print("")
print("Results:")
string_total = "probabilites total           : "
string_total += str(total_prob)
print(string_total) 
string_total = "no probabilites determined   : "
string_total += str(no_prob)
print(string_total)   
string_total = "probabilites equals 0.1      : "
string_total += str(final_prob_0)
print(string_total)
string_total = "probabilites equals 0.9      : "
string_total += str(final_prob_1)
print(string_total)
string_total = "probabilites equals 0.5      : "
string_total += str(final_prob_5)
print(string_total)
string_total = "probabilites greater than 0.5: "
string_total += str(final_prob_gt)
print(string_total)
string_total = "probabilites lesser than 0.5 : "
string_total += str(final_prob_lt)
print(string_total)
print("")
print("additional information")
string_total = "total tokens                 : "
string_total += str(len(probabilities))
print(string_total)
string_total = "previosly uknown tokens      : "
string_total += str(unknown_probs)
print(string_total)
    
