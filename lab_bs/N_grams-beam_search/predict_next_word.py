import random


dabile = {}


def texts_Compare_similarity(ls_text1, ls_text2):
    ata = 0
    ls_text2_t = list(ls_text2)
    bso = len(ls_text2_t)
    list_id = []
    for val in ls_text1:
        if val in ls_text2_t:
            ata += 1
            key = ls_text2_t.index(val)
            ls_text2_t[key] = "*"
            list_id.append(key)
    return [ata, bso, list_id]


def highest_probability(piece_text, piece_list):
    atast = []
    qes_ui_len = len(piece_text)
    for x in piece_list:
        piba = texts_Compare_similarity(piece_text, x)
        le_1 = 0
        le_2 = 0
        len_pi_id = len(piba[2])-1
        for key, val in enumerate(piba[2]):
            if key == len_pi_id:
                break
            if val+1 == piba[2][key+1]:
                le_1 += 1
            if val < piba[2][key+1]:
                le_2 += 1
        if piba[0] == 0:
            atast.append(0)
        else:
            atast.append((0.57*(piba[0]/piba[1]) + 0.29*(le_2/piba[0]) + 0.14*(le_1/piba[0]))*(piba[0]/qes_ui_len))
    return atast.index(max(atast))


with open('a_mod_lit_f.txt', "r", encoding="utf-16") as file:
    for line in file:
        line_t = line.split("\t", 2)
        key = line_t[0]
        value = [line_t[1].split(",") , line_t[2].replace("\n", "").split(",")]
        val_end = []
        for ind, val in enumerate(value[0]):
            val_end.append([val, value[1][ind]])
        dabile[key] = val_end

dabile_key = list(dabile.keys())
dabile_key_df = list(dabile.keys())
for ind, val in enumerate(dabile_key):
    dabile_key[ind] = list(val)


def guess_word(text):
    text_n = text.split()
    if len(text) > 3:
        text_n = text_n[-3:]
    text_dp = " ".join(text_n)
    text_dp = list(text_dp.lower())
    while(len(text_n) > 0):
        text = " ".join(text_n)
        if text in dabile:
            det = [[text], dabile[text]]
            break
        text_n.pop(0)
    if len(text_n) == 0:
        tex_dc = dabile_key_df[highest_probability(text_dp, dabile_key)]
        det = [[tex_dc], dabile[tex_dc]]
    net_lt = 6
    cap_v = 0.7
    det[1].sort(key=lambda s: s[1], reverse=True)
    if len(det[1]) > net_lt:
        nat = int(net_lt*cap_v)
        det[1] = det[1][:nat] + random.choices(det[1][nat:], k=net_lt-nat)
        valueb = []
        for x in det[1]:
            valueb.append(x[0])
        det[1] = valueb
    return det




tex = "đưa lên sàn_"
print(guess_word(tex))