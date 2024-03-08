from permutation import Permutation
from language_model import CorpusReader, LanguageModel
from simulated_annealing import SimulatedAnnealing

import string
T = ",.:\n#()!?\'\""
global Sigma
Sigma = string.ascii_lowercase + T + " "

url_gut = "https://www.gutenberg.org/files/76/76-0.txt"
corpus = CorpusReader(url_gut)
gut_model = LanguageModel(corpus)

path = input("provide encrypted message path \n If in current dir, file name is enough")
if not path.lower().endswith(".txt"):
    path += ".txt"
encrypt_file = open(path,"r")
encrypted_message = ''.join(line for line in encrypt_file.readlines())

initial_permutation = Permutation(Sigma)

initemp = float(input("provide initial temperature"))
thrsh = float(input("provide threshold"))
cool_rate = float(input("provide cooling rate"))

sim_aneal = SimulatedAnnealing(initemp,thrsh,cool_rate)

encryption = sim_aneal.run(initial_permutation,encrypted_message,gut_model)
# a Permutation type object

print("\nwinning permutation: \n" + encryption.perm)
print("\ninitial temperature = " + str(initemp) + ",\tthreshold = " + str(thrsh) + ",\t cooling rate used = " + str(cool_rate))
print("\ndeciphered message = \n" + encryption.translate(encrypted_message))
