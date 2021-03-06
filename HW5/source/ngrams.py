from __future__ import division
from operator import itemgetter
import sys
import re
import math


class NGrams:
  def __init__(self):
    self.uni_dict = {}
    self.unitypes = 0
    self.unitokens = 0
    self.bi_dict = {}
    self.bitypes = 0
    self.bitokens = 0
    self.tri_dict = {}
    self.tritypes = 0
    self.tritokens = 0

    self.logProbs = 0
    self.sentNum = 0
    self.wordNum = 0
    self.oovNum = 0
    self.pplNum = 0


  def avg_lgprob(self):
### average logprob = number of sentences + total number of words - number of out of vocabulary words
    return self.logProbs / (self.wordNum + self.sentNum - self.oovNum)


  def ppl_calc(self):
### perplexity of the text = 10 to the power of negative average logprob
    return math.pow(10, -self.avg_lgprob())


  def BOS_EOS(self, line):
### insert beginning and end of string tags
    line = "<s> " + line.strip() + " </s>" + '\n'
    return line


  def count_unigrams(self, text):
### get unigrams; stuff in the dictionary; count and sort 
    for token in text.split(): #list_all.split():
      if not token in self.uni_dict:
        self.uni_dict[token] = 1
      else:
        self.uni_dict[token] = self.uni_dict[token] + 1
### reverse sort by frequency
    self.uni_dict = sorted(self.uni_dict.items(), key = lambda a: -a[1])
    return self.uni_dict
   

  def count_bigrams(self, text):
### get bigrams; stuff in the dictionary; count; sort
    t = text.split()   # list_all

    for i in range(0, len(t)-1):

      bigram = t[i] + ' ' + t[i+1]
### adding bigrams to dict if the first element is not </s>
      if not bigram in self.bi_dict and not t[i] == '</s>':
        self.bi_dict[bigram] = 1
      elif t[i] == '</s>':
        continue
      else:
        self.bi_dict[bigram] = self.bi_dict[bigram] + 1

    self.bi_dict = sorted(self.bi_dict.items(), key = lambda a: -a[1])
    return self.bi_dict 
   

  def count_trigrams(self, text):
### count trigrams
    t = text.split()   
    for i in range(0, len(t)-2):
      trigram = t[i] + ' ' + t[i+1] + ' ' + t[i+2]
      if not trigram in self.tri_dict and not (t[i] == '</s>' or t[i+1] == '</s>'):
        self.tri_dict[trigram] = 1
      elif (t[i] == '</s>' or t[i+1] == '</s>'):
        continue
      else:
        self.tri_dict[trigram] = self.tri_dict[trigram] + 1

    self.tri_dict = sorted(self.tri_dict.items(), key = lambda a: -a[1])
    return self.tri_dict


  def read_into_dicts(self, line_of_input):
### reading ngram_count_file into a data structure line by line: ngram is key; frequency is value
    ilist = re.split('\s+', line_of_input.strip())

    if len(ilist) == 2:
      self.uni_dict[ilist[1]] = int(ilist[0])
    elif len(ilist) == 3:
      key = ' '.join(ilist[1:])
      self.bi_dict[key] = int(ilist[0])    
    elif len(ilist) == 4:
      key = ' '.join(ilist[1:])
      self.tri_dict[key] = int(ilist[0])


  def count_types_tokens(self, dictionary):
### count how many types and how many tokens
    types = len(dictionary)
    tokens = sum(dictionary.values())

    return (types, tokens)
 

  def calc_uni_prob(self):
### calculate probability and logprob and return it all as a list together with the count and the n-gram
    ARPA = []
    for key in self.uni_dict:
      prob = self.uni_dict[key]/self.count_types_tokens(self.uni_dict)[1]
      logprob = math.log10(prob)     
      ARPA.append([self.uni_dict[key], prob, logprob, key])

    return sorted(ARPA, key = itemgetter(0), reverse = True)


  def calc_bi_prob(self):
### calculate conditional probability for bigrams
    ARPA = []
    for key in self.bi_dict:
      keyparts = key.split()
      prob = self.bi_dict[key]/self.uni_dict[keyparts[0]]
      logprob = math.log10(prob)
      ARPA.append([self.bi_dict[key], prob, logprob, key])
    return sorted(ARPA, key = itemgetter(0), reverse = True)


  def calc_tri_prob(self):
### calculate conditional probability for bigrams
    ARPA = []
    for key in self.tri_dict:
      keyparts = key.split()

      bigram = ' '.join(keyparts[0:2])
      prob = self.tri_dict[key]/self.bi_dict[bigram]
      logprob = math.log10(prob)
      ARPA.append([self.tri_dict[key], prob, logprob, key])

    return sorted(ARPA, key = itemgetter(0), reverse = True)


  def read_lm_file_into_dicts(self, line_of_input):
### reading lm_file into a dictionary line by line; have to start reading from line 6 of file; will have to be done in main()
### out of four elements we need [1] - prob -- value in the dictionary
### and [3] - ngram -- key in the dictionary
    ilist = re.split('\s+', line_of_input.strip())
    if len(ilist) == 4:
      self.uni_dict[ilist[3]] = ilist[1]
    elif len(ilist) == 5:
      key = ' '.join(ilist[3:])
      self.bi_dict[key] = ilist[1]
    elif len(ilist) == 6:
      key = ' '.join(ilist[3:])
      self.tri_dict[key] = ilist[1]
    else:
      return None


  def Perplexity(self, sentence, l1, l2, l3, j):   
### l1, l2, l3 - for interpolation; passed from main
    
    print '\nSent #' + str(j) + ': ' + sentence

    notfound = False
 
    s = sentence.split()
    sumP = 0
    OOV = 0

### processing the first bigram
    P1 = 0
    first_bi = ' '.join(s[0:2])
    if first_bi in self.bi_dict:
      P1 = l2 * float(self.bi_dict[first_bi])
    else:
      P1 = (0)
      notfound = True

### is the unigram s[1] in the language model?
    if s[1] in self.uni_dict:
      P1 = P1 + l1 * float(self.uni_dict[s[1]])
      logP1 = math.log10(P1)
      if notfound == True:
        print '1: lg P(' + s[1] + ' | ' + s[0] + ') = ' + str(logP1) + ' (unseen ngrams)'
      else:
        print '1: lg P(' + s[1] + ' | ' + s[0] + ') = ' + str(logP1)
### if not in lm, then the probability is zero and out of vocabulary count is incremented        
    else:
      P1 = (0)
      OOV += 1
      
      print '1: lg P(' + s[1] + ' | ' + s[0] + ') = -inf (unknown word)'
    if not P1 == 0:
      sumP = sumP + logP1 

### repeating the same procedure - now for all the trigrams in the sentence
    wordcount = 0
    trigramNumber = 2     

    for i in range(0, len(s)-2):
 
      P = (0)
      notfound = False
      tri = ' '.join([s[i], s[i+1], s[i+2]])
    
      if tri in self.tri_dict:
        P = l3 * float(self.tri_dict[tri])
      else:
        P = (0)
        notfound = True
### checking if the bigram is in the language model      
      bi = ' '.join([s[i+1], s[i+2]])
      if bi in self.bi_dict:
        P = P + l2 * float(self.bi_dict[bi])
      else:
        P = P + 0
        notfound = True
### checking if the unigram is in the language model       
      uni = s[i+2]

      if uni in self.uni_dict:
        P = P + l1 * float(self.uni_dict[uni])
        logP = math.log10(P)
        if notfound == True:
          print str(trigramNumber) + ': lg P(' + s[i+2] + ' | ' + s[i] + ' ' + s[i+1] + ') = ' + str(logP) + ' (unseen ngrams)'
        else:
          print str(trigramNumber) + ': lg P(' + s[i+2] + ' | ' + s[i] + ' ' + s[i+1] + ') = ' + str(logP)
      else:
        P = P + 0
        
        OOV += 1
        print str(trigramNumber) + ': lg P(' + s[i+2] + ' | ' + s[i] + ' ' + s[i+1] + ') = -inf (unknown word)'
### taking the logprob of the non-zero probability of the n-gram and adding to the probability of the sentence    
      if not P == 0:
        sumP += math.log10(P)  
      
      wordcount += 1
      trigramNumber += 1     

    print '1 sentence, ' + str(wordcount) + ' words, ' + str(OOV) + ' OOVs'
    total = -sumP / wordcount
    ppl = math.pow(10, total) 

    print 'lgprob=' + str(sumP) + ' ppl=' + str(ppl) + '\n\n'
### summary counts for the output
    self.logProbs += sumP
    self.sentNum += 1
    self.wordNum += wordcount
    self.pplNum += ppl
    self.oovNum += OOV

    return ppl



