# Authors: Alex Warstadt
# Functions for accessing vocab matrices

import numpy as np
import utils.verb_data_type
import re
import os

'''Dictionary,CONJ,POS,Mood,Tense,Person,Number,Aspect,Gender,category,category_2,arg_1,arg_2,arg_3,root,wh_np_verb,responsive,passive,strict_intrans,strict_trans,causative,spray_load,inchoative,agentive,frontable,irr_verb,negated,arg_clause,homophonous,v_embed_sc,change_of_state,initial_state,change_arg'''



data_type = [("Infinitive", "U100000"),
             ("CONJ", "U10000"),
             ("POS", "U20"),
             ("Reflexive","U1"),
             ("Mood", "U10"),
             ("Tense", "U10"),
             ("Person", "U1"),
             ("Number", "U2"),
             ("Apect", "U20"),
             ("Gender", "U10"),
             ("category", "U20"),
             ("category_2", "U20"),
             ("arg_1", "U100"),
             ("arg_2", "U100"),
             ("arg_3", "U100"),
             ("root", "U20"),
             ("wh_np_verb", "U1"),
             ("responsive", "U1"),
             ("passive", "U1"),
             ("strict_intrans", "U1"),
             ("strict_trans", "U1"),
             ("causative", "U1"),
             ("spray_load", "U1"),
             ("inchoative", "U1"),
             ("agentive", "U1"),
             ("frontable", "U1"),
             ("irr_verb", "U100"),
             ("negated", "U100"),
             ("arg_clause", "U100"),
             ("homophonous", "U1"),
             ("v_embed_sc", "U1"),
             ("change_of_state", "U1"),
             ("initial_state", "U1000"),
             ("change_arg", "U1")
            ]



#vocab_path = os.path.join("/".join(os.path.join(os.path.dirname(os.path.abspath#(__file__))).split("/")[:-1]), "vocabulary.csv")
vocab_path = "./csv_test.csv"
vocab = np.genfromtxt(vocab_path, delimiter=",", names=True, dtype=data_type)
#print(vocab)
# decode TODO: make this not a hack
for entry in vocab:
    entry[0] = re.sub("!", "'", entry[0])


def get_all(label, value, table=vocab):
    """
    :param label: string. field name.
    :param value: string. label.
    :param table: ndarray of vocab items.
    :return: table restricted to all entries with "value" in field "label"
    """
    # TODO: this should not be based on string equality, but disjunction matching
    # return np.array(list(filter(lambda x: condition_is_match_disj(value, x[label]), table)), dtype=data_type)
    return np.array(list(filter(lambda x: x[label] == value, table)), dtype=table.dtype)

def get_all_conjunctive(labels_values, table=vocab):
    """
    :param labels_values: list of (l,v) pairs: [(l1, v1), (l2, v2), (l3, v3)]
    :return: vocab items with the given value for each label
    """
    to_return = table
    for label, value in labels_values:
        to_return = np.array(list(filter(lambda x: x[label] == value, to_return)), dtype=table.dtype)
    return to_return


def get_matches_of(row, label, table=vocab):
    """
    :param row: ndarray row. functor vocab item.
    :param label: string. field containing selectional restrictions.
    :param table: ndarray of vocab items.
    :return: all entries in table that match the selectional restrictions of row as given in label.
    """
    value = str(np.array(row, dtype=table.dtype)[label])
    if value == "":
        pass
    else:
        matches = []
        values = str(value).split(";")
        for disjunct in values:
            k_vs = conj_list(disjunct)
            matches.extend(list(get_all_conjunctive(k_vs, table)))
        return np.array(matches, dtype=table.dtype)


def get_matches_of_conj(rows_labels, table=vocab):
    """
    :param rows_labels: list of (r,l) pairs: [(r1, l1), (r2, l2), (r3, l3)]
    :param table: ndarray of vocab items.
    :return: all entries in table that match the selectional restrictions of all rows as given by labels.
    """
    to_return = table
    for row, label in rows_labels:
        value = str(np.array(row, dtype=table.dtype)[label])
        if value == "":
            pass
        else:
            to_return = np.array(list(filter(lambda x: is_match_disj(x, value), to_return)), dtype=table.dtype)
    return to_return


def get_matched_by(row, label, table=vocab):
    """
    :param row: ndarray row. selected vocab item.
    :param label: string. field containing selectional restrictions.
    :param table: ndarray of vocab items.
    :return: all entries in table whose selectional restrictions in label are matched by row.
    """
    matches = []
    for entry in table:
        value = str(np.array(entry, dtype=table.dtype)[label])
        if is_match_disj(row, value):
            matches.append(entry)
    return np.array(matches)


def conj_list(conjunction):
    """
    :param disjunct: a string corresponding to a conjunction of selectional restrictions
    :return: a list of k, v pairs 
    """
    try:
        to_return = [(v.split("=")[0], v.split("=")[1]) for v in conjunction.split("^")]
        return to_return
    except IndexError:
        pass

def is_match_disj(row, disjunction):
    """
    :param row: a vocab item
    :param disjunction: a string corresponding to a disjunction of selectional restrictions
    :return: true if the row matches one of the disjuncts, false otherwise
    """
    if disjunction == "":
        return True
    else:
        disjuncts = disjunction.split(";")
        match = False
        for d in disjuncts:
            match = match or is_match_conj(row, d)
        return match

def is_match_conj(row, conjunction):
    """
    :param row: a vocab item
    :param conjunction: a string corresponding to a conjunction of selectional restrictions
    :return: true if the row matches the conjunction, false otherwise
    """
    conjuncts = conj_list(conjunction)
    match = True
    for k, v in conjuncts:
        try:
            match = match and row[k] == v
        except TypeError:
            pass
    return match

def condition_is_match_disj(condition, disjunction):
    """
    :param condition: a string representing a selectional condition
    :param disjunction: a string corresponding to a disjunction of selectional restrictions
    :return: true if the row matches one of the disjuncts, false otherwise
    """
    if disjunction == "":
        return True
    else:
        disjuncts = disjunction.split(";")
        match = False
        for d in disjuncts:
            match = match or condition_is_match_conj(condition, d)
        return match

def condition_is_match_conj(condition, conjunction):
    """
    :param condition: a string representing a selectional condition
    :param conjunction: a string corresponding to a conjunction of selectional restrictions
    :return: true if the row matches the conjunction, false otherwise
    """
    conjuncts = conj_list(conjunction)
    match = True
    for k, v in conjuncts:
        try:
            match = match and condition[k] == v
        except TypeError:
            pass
    return match
