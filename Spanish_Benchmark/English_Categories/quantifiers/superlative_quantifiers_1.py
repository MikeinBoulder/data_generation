from Spanish_Utils.randomize import choice
from Spanish_Utils.vocab_sets import *
from Spanish_Utils.string_utils import *
import numpy as np
#all_singular_count_nouns
#all_trans_p3is
#all_p3is_anim_subj_allowing_verbs
#all_singular_count_nouns_fem
quantifiers = [("mas que", "al menos"),
               ("menos que", "como mucho")]
numbers = ['dos','tres','quatro','cinco','seis','siete','ocho','nueve']
ningun_masc = 'ningún'
ningun_fem = 'ningúna'
safe_nouns = np.setdiff1d(all_plural_nouns, all_proper_names)

def sample(iter, out):
        # No professor graded more than three papers
        # NO N1        V      Q1        Num   N2
        # No professor graded at least four papers
        # NO N1        V      Q2       Num  N2
    for i in range(iter):
        V = choice(all_trans_p3is)
        if choice([True,False]):
            ningun = ningun_fem
            N1 = choice(all_singular_count_nouns_fem)
        else:
            ningun = ningun_masc
            N1 = choice(all_singular_count_nouns_masc)
        N2 = choice(safe_nouns)
        quantifiers = random.choice(quantifiers)
        Q1 = quantifiers[0]
        Q2 = quantifiers[1]
        Num = choice(numbers)
        data = {
            "sentence_good": "%s %s %s %s %s %s %s." % (ningun, N1, V, Q1, Num, N2),
            "sentence_bad": "%s %s %s %s %s %s %s." % (ningun, N1, V, Q2, Num, N2),
        }
    print(data)
