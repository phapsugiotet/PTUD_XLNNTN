import os
import re
from nltk import ngrams
from underthesea import word_tokenize

def ta_lat(list_tx, tcut):
    list_pn = []
    for x in list_tx:
        list_pn += x.split(tcut)
    return list_pn


def get_n_grams(texts, n=5):
    n_grams = ngrams(texts, n)
    n_grams_ls = []
    for grams in n_grams:
        n_grams_ls.append(list(grams))
    return n_grams_ls


WORD_LENGTH = 3


file_list = []
for (dirpath, dirname, filename) in os.walk('Train_Full'):
    for f in filename:
        file_list.append(dirpath+'/'+f)
print(len(file_list))
sequences = []
for f in file_list:
    with open(f, encoding="utf-16", errors='ignore') as x:
        text = x.read().lower()
        sequences.append(text)

print("sta")
# print(sequences)
sequences = ta_lat(sequences, "\n")
sequences = ta_lat(sequences, ".")
sequences = ta_lat(sequences, ",")
print("cret")
for w_l in range(1, WORD_LENGTH+1):
    print("echo =", w_l, end="  ")
    stras = []
    for x in sequences:
        x = re.sub('\s', ' ', re.sub('\W+', ' ', x))
        x = x.split()
        x = get_n_grams(x, w_l+1)
        stras += x

    stras_t = []
    for x in stras:
        if len(x) > 0:
            x = x[:w_l] + [word_tokenize(" ".join(x[-2:]))[0]]
            stras_t.append(x)
    print("stras", end="  ")
    # print(stras_t)
    n_grams_ls = {}
    for grams in stras_t:
        grams_k = " ".join(grams[0:-1])
        if grams_k in n_grams_ls:
            xa = list(n_grams_ls[grams_k])
            n_grams_ls[grams_k] = xa+[grams[w_l]]
        else:
            n_grams_ls[grams_k] = [grams[w_l]]

    # print(n_grams_ls)
    print("n_grams_ls", end="  ")

    for k, value in n_grams_ls.items():
        kafa = 0
        valack = []
        valdet = []
        for x in value:
            if x in valack:
                valdet[valack.index(x)]=valdet[valack.index(x)]+1
            else:
                valack.append(x)
                valdet.append(0)
        n_grams_ls[k] = [valack, valdet]
    print("n_grams_eu", end="  ")
    # print(n_grams_ls)
    n_grams_lse = {}
    for k, value in n_grams_ls.items():
        valack = []
        valdet = []
        for ind, val in enumerate(value[0]):
            if not val.isdecimal():
                valack.append(val)
                valdet.append(value[1][ind])
        if len(valack) != 0 and (not re.search(r'\d', k)):
            n_grams_lse[k] = [valack, valdet]
    print("ato ", end=" ")
    file = open("a_mod_lit_f_w_tk.txt", "a", encoding="utf-16")
    for k, value in n_grams_lse.items():
        string_ints = [str(int) for int in value[1]]
        file.write(k + "\t" + ",".join(value[0]) + "\t" + ",".join(string_ints)+"\n")
    print("at: ", w_l)



# sequences = re.sub('\s', ' ', re.sub('\W+', ' ', sequences))
# sequences = sequences.split()
# sequences = ngrams(sequences, 3)
# n_grams_ls = {}
#
# for grams in sequences:
#     if grams[0]+" "+grams[1] in n_grams_ls:
#         xa = list(n_grams_ls[grams[0]+" "+grams[1]])
#         n_grams_ls[grams[0]+" "+grams[1]] = xa+[grams[2]]
#     else:
#         n_grams_ls[grams[0]+" "+grams[1]] = [grams[2]]
#         # print(grams[2])
#
# for k, value in n_grams_ls.items():
#     value = set(value)
#     value = list(value)
#     n_grams_ls[k] = value
#
# print(n_grams_ls)
# print("-"*20)
#
# file = open("demofile2.txt", "w", encoding="utf-16")
# for k, value in n_grams_ls.items():
#     file.write(k +"\t"+ ",".join(value)+"\n")
#
#
# dabile = {}
# with open('demofile2.txt', "r", encoding="utf-16") as file:
#     for line in file:
#         line_t = line.split("\t", 1)
#         key = line_t[0]
#         value = line_t[1].replace("\n", "").split(",")
#         dabile[key] = value
#
# print(dabile)
