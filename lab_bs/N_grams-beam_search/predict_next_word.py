import random


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
            atast.append((0.57*(piba[0]/piba[1]) + 0.29*(le_1/piba[0]) + 0.14*(le_2/piba[0]))*(piba[0]/qes_ui_len))
    return atast.index(max(atast))


dabile = {}

WORD_LENGTH = 2

with open('a_mod_lit_f.txt', "r", encoding="utf-16") as file:
    for line in file:
        line_t = line.split("\t", 2)
        key = line_t[0]
        if len(key.split()) > WORD_LENGTH:
            continue
        value = [line_t[1].split(","), line_t[2].replace("\n", "").split(",")]
        val_end = []
        for ind, val in enumerate(value[0]):
            val_end.append([val, value[1][ind]])
        dabile[key] = val_end

dabile_key = list(dabile.keys())
dabile_key_df = list(dabile.keys())
for ind, val in enumerate(dabile_key):
    dabile_key[ind] = list(val)


def guess_word(text, net_lt, len_n=2, approximately=False):
    if text =='':
        return []
    text_cp = text[-1:]
    text_n = text.split()
    if len(text) > len_n:
        text_n = text_n[-len_n:]
    text_dp = " ".join(text_n)
    text_dp = list(text_dp.lower())
    con_c = 0
    while(len(text_n) > 0):
        text = " ".join(text_n)
        if text in dabile:
            con_c = 1
            det = [[text, con_c], dabile[text]]
            break
        det_tt = []
        for ind in dabile:
            if ind.startswith(text):
                det_tt.append([ind, 0])
                con_c = 2
                # break
        if con_c == 2:
            det = [[text, con_c], det_tt]
            break
        text_n.pop(0)
    if len(text_n) == 0:
        if not approximately:
            return []
        text_p = highest_probability(text_dp, dabile_key)
        tex_dc = dabile_key_df[text_p]
        det = [[tex_dc, con_c], dabile[tex_dc]]
        # return None
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


def predict_next_word(text, net_lt, len_n=2, approximately=False):
    pas = [" ", ""]
    if text[-1] == " ":
        pas = ["", " "]
    prediction_list = []
    prediction_op = guess_word(text.lower(), net_lt, len_n, approximately)
    if len(prediction_op) == 0:
        for i in range(net_lt):
            prediction_list.append(["", ""])
        return prediction_list
    if prediction_op[0][1] == 1:
        for ind in prediction_op[1]:
            prediction_list.append([ind, pas[0]+ind])
    elif prediction_op[0][1] == 2:
        for ind in prediction_op[1]:
            prediction_list.append([ind, ind.replace(prediction_op[0][0], "", 1)])
    if len(prediction_list) >= net_lt:
        return prediction_list[0:net_lt]
    pre_list = prediction_op[0][0].split()
    if len(pre_list) > 1:
        pre_list.pop(0)
        prediction_list += predict_next_word(" ".join(pre_list)+pas[1], net_lt*2, len_n, approximately)
        detra = []
        detro = []
        for x in prediction_list:
            if not x[0] in detra:
                detro.append(x)
                detra.append(x[0])
        prediction_list = detro[0:net_lt]
    for i in range(net_lt - len(prediction_list)):
        prediction_list.append(["", ""])
    return prediction_list



tex = "hoa mai là một bông w"
print(tex)
print(predict_next_word(tex.lower(), 6, WORD_LENGTH))