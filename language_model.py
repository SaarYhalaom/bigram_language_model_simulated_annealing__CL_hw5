import math
import urllib.request

import string
T = ",.:\n#()!?\'\""
global Sigma
Sigma = string.ascii_lowercase + T + " "


class CorpusReader:
    global Sigma #alphabet, for use in class

    """char generator:
    takes a url to a txt file,
    and yields the chars in the file,
    in lowercase & if in {a, b, c, ..., z} ∪ {space} ∪ T
    """
    def txt_url_to_char_generator(self,url):
        data = urllib.request.urlopen(url)
        for line in data:
            line_str = line.decode('utf-8').lower()
            for char in line_str:
                if char in Sigma:
                    yield char

    def __init__(self,url):
        self.txt = ''.join(char for char in self.txt_url_to_char_generator(url))


class LanguageModel:
    global Sigma #alphabet, for use in class

    """takes a CorpusReader instance, and returns a 2-tuple of dicts:
    (uni_count_dict, bi_count_dict)
     """
    def count_to_dict(self,corpus):
        uni_count_dict = {}
        bi_count_dict = {}

        #counting instances of chars for uni_count_dict
        for char in corpus.txt:
            if char in uni_count_dict:
                uni_count_dict[char] += 1
            else:
                uni_count_dict[char] = 1

        #adding any missing chars
        for char in Sigma:
            if char not in uni_count_dict:
                uni_count_dict[char] = 0

        #counting instances of pairs for bi_count_dict
        for i in range(len(corpus.txt)):
            pair = corpus.txt[i:i+2]
            if pair in bi_count_dict:
                bi_count_dict[pair] += 1
            else:
                bi_count_dict[pair] = 1

        #adding any missing pairs
        for char1 in Sigma:
            for char2 in Sigma:
                pair = char1 + char2
                if pair not in bi_count_dict:
                    bi_count_dict[pair] = 0

        return (uni_count_dict, bi_count_dict)


    """takes a 2-tuple of dicts: (uni_count_dict, bi_count_dict)
    and re-writes (in-place) their info-s as MLE probs
    applies Laplace smoothing"""
    def uni_count_to_MLE(self,dicts):
        uni_count_dict, bi_count_dict = dicts

        # getting overall char-count
        N = 0
        for char in uni_count_dict:
            N += uni_count_dict[char]

        # switching bi-counts with MLE probs
        for pair in bi_count_dict:
            bi_count_dict[pair] = (bi_count_dict[pair] + 1) / (uni_count_dict[pair[0]] + len(Sigma))

        # switching uni-counts with MLE probs
        for char in uni_count_dict:
            uni_count_dict[char] = (uni_count_dict[char] + 1) / (N + len(Sigma))

        return None

    """corpus is a CorpusReader instance"""
    def __init__(self,corpus):
        uni_dict, bi_dict = self.count_to_dict(corpus)
        self.uni_count_to_MLE((uni_dict, bi_dict))

        self.uni_dict = uni_dict
        self.bi_dict = bi_dict
        self.old_dicts = None #used in logging & de-logging model, see below

    """turns every prob in a model to -log_2^(val),
    used for simulated annealing optimization (not to calc log again every time)
    stores a copy of old dictionaries as old_dicts for de-logging"""
    def log_model(self):
        logged_uni_dict = {}
        logged_bi_dict = {}

        for key in self.uni_dict:
            logged_uni_dict[key] = math.log(self.uni_dict[key],2)
        for key in self.bi_dict:
            logged_bi_dict[key] = math.log(self.bi_dict[key],2)

        self.old_dicts = (self.uni_dict, self.bi_dict)
        self.uni_dict = logged_uni_dict
        self.bi_dict = logged_bi_dict

    """returning prob values to pre-logging, after log_model(self)
    used when wrapping up simulated annealing"""
    def de_log_model(self):
        self.uni_dict, self.bi_dict = self.old_dicts
        self.old_dicts = None #just for good measures and memory frugality
