import string
T = ",.:\n#()!?\'\""
global Sigma
Sigma = string.ascii_lowercase + T + " "

class Permutation:
    global Sigma #alphabet, for use in class

    """permutations are represented as a
    permutated version of Sigma"""
    def __init__(self,perm):
        self.perm = perm

    def get_neighbor(self):
        import random

        perm = self.perm
        i = random.randint(0, len(perm)-2)
        j = random.randint(i+1, len(perm)-1)
        # i < j

        new_perm = perm[0:i] + perm[j] + perm[i+1:j] + perm[i] + perm[j+1:]
        return Permutation(new_perm)


    def translate(self,txt):
        return ''.join(self.perm[Sigma.index(char)] for char in txt)
        # using perm as a direct representation of the permutation:
        # for each char, find its index in Sigma, than take the letter
        # in perm w/ same index


    """
    @pre: txt (encrypted massage) of length of at least 2
    @pre: model was already logged with LanguageModel.log_model()"""
    def get_energy(self,txt,model):
        import math

        txt = self.translate(txt)

        eng = model.uni_dict[txt[0]]
        # initializing eng with probability of first char

        for i in range(len(txt)-1):
            eng += model.bi_dict[txt[i:i+2]]

        return 0 - eng