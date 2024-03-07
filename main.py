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

path = input("provide encrypted massage path \n If in current dir, file name is enough")
if not path.lower().endswith(".txt"):
    path += ".txt"
encript_file = open(path,"r")
encripted_massage = ''.join(line for line in encript_file.readlines())

initial_permutation = Permutation(Sigma)

initemp = float(input("provide initial temperature"))
thrsh = float(input("provide threshold"))
cool_rate = float(input("provide cooling rate"))

sim_ameal = SimulatedAnnealing(initemp,thrsh,cool_rate)

encription = sim_ameal.run(initial_permutation,encripted_massage,gut_model)
# a Permutation type object

print("\nwinning permutation: " + encription.perm)
print("\ninitial temperature = " + str(initemp) + ",\tthreshold = " + str(thrsh) + ",\t cooling rate used = " + str(cool_rate))
print("\ndeciphered message = " + encription.translate(encripted_massage))
