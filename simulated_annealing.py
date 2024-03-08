import math
import random

class SimulatedAnnealing:
    def __init__(self,initemp,thrsh,cool_rate):
        self.initemp = initemp
        self.thrsh = thrsh
        self.cool_rate = cool_rate

    def run(self,perm,txt,model):
        model.log_model() # log all values once, instead of repeatedly

        D = txt
        H = perm
        T = self.initemp
        while T > self.thrsh:
            new_H = H.get_neighbor()
            new_eng = new_H.get_energy(D,model)
            old_eng = H.get_energy(D,model)
            delta = new_eng - old_eng
            if delta < 0:
                p = 1
            else:
                p = math.exp(0 - delta / T)
            r = random.random()
            if r < p:
                H = new_H
            T = T * self.cool_rate

        model.de_log_model() # for good measures, returning model to pre-logged state

        return H

