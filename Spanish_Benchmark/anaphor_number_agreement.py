from Spanish_Utils.vocab_sets import *
import numpy as np
from Spanish_Utils.randomize import choice
import random


def sample(max_iter):
        for i in range(max_iter):
                #plural verb
                if choice([True, False]):
                        V = choice(verbs_p3ip)
                        #fem pl noun
                        if choice([True,False]):
                                D = choice(d_fem_pl)
                                N = choice(n_fem_pl)
                                rp_good = pl_reflexives[1]
                                #all_reflexives.remove(rp_good)
                                rp_bad = sg_reflexives[1]
                                #all_reflexives.insert(3, rp_good)
                        else:
                                D = choice(d_masc_pl)
                                N = choice(n_masc_pl)
                                rp_good = pl_reflexives[0]
                                #all_reflexives.remove(rp_good)
                                rp_bad = sg_reflexives[0]
                                #all_reflexives.insert(2, rp_good)

                #singular verb
                else:
        
                        V = choice(verbs_p3is)
                        #fem sg noun
                        if choice([True,False]):
                                D = choice(d_fem_sg)
                                N = choice(n_fem_sg)
                                rp_good = sg_reflexives[1]
                                #all_reflexives.remove(rp_good)
                                rp_bad = pl_reflexives[1]
                                #all_reflexives.insert(1, rp_good)
                        else:
                                D = choice(d_masc_sg)
                                N = choice(n_masc_sg)
                                rp_good = sg_reflexives[0]
                                #all_reflexives.remove(rp_good)
                                rp_bad = pl_reflexives[0]
                                #all_reflexives.insert(0,rp_good)
                                                               
                #Verb fix
                if not V.startswith('se', 0, 2):
                        V = 'se ' + V
                                        
                                        
                                        
                if N[0] >= 'A' and N[0] <= 'Z':
                        data = {
                                "sentence_good": "%s %s %s." % (N, V, rp_good),
                                "sentence_bad": "%s %s %s." % (N, V, rp_bad)
                        }
                else:
                        data = {
                                "sentence_good": "%s %s %s %s." % (D, N, V, rp_good),
                                "sentence_bad": "%s %s %s %s." % (D, N, V, rp_bad)
                        }
                print(data)

sample(10)



