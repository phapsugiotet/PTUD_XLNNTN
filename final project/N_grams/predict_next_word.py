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


def custom_random(listz, weightsx, ky):
    if len(listz) == ky:
        return listz
    safa = random.choices(listz, weights=weightsx, k=ky)
    safa = list(set(safa))
    len_co = ky - len(safa)
    if len_co > 0:
        for ind in safa:
            id = listz.index(ind)
            listz.pop(id)
            weightsx.pop(id)
        return safa + custom_random(listz, weightsx, len_co)
    return safa

def guess_word(text, net_lt, len_n=2, approximately=False):
    if text == '':
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
        det_te = []
        for ind in dabile:
            if ind.startswith(text):
                det_tt.append(ind)
                det_te.append(1)
                con_c = 2
                # break
        if con_c == 2:
            det = [[text, con_c], [det_tt, det_te]]
            break
        text_n.pop(0)
    if len(text_n) == 0:
        if not approximately:
            return []
        text_p = highest_probability(text_dp, dabile_key)
        tex_dc = dabile_key_df[text_p]
        det = [[tex_dc, con_c], [dabile[tex_dc], [1]]]
        # return None
    len_det = len(det[1][0])
    if len_det > net_lt:
        det[1] = custom_random(list(det[1][0]), list(det[1][1]), net_lt)
        # print("map 2", det)
        return det
    det[1] = custom_random(list(det[1][0]), list(det[1][1]), len_det)
    # print("map 1", det)
    return det


def predict_next_word(text, net_lt, len_n=2, approximately=False):
    prediction_list = []
    text_nt = text.split()[-1]
    if text_nt.isupper():
        text_nt = 1
    elif text_nt[0].isupper():
        text_nt = 2
    else:
        text_nt = 0
    prediction_op = guess_word(text.lower(), net_lt, len_n, approximately)
    if len(prediction_op) == 0:
        for i in range(net_lt):
            prediction_list.append(["", ""])
        return prediction_list
    pas = [" ", ""]
    if text[-1] == " ":
        pas = ["", " "]
    if text_nt == 2:
        prediction_op[0][0] = prediction_op[0][0].title()
        for ind, val in enumerate(prediction_op[1]):
            prediction_op[1][ind] = val.title()
    if text_nt == 1:
        prediction_op[0][0] = prediction_op[0][0].upper()
        for ind, val in enumerate(prediction_op[1]):
            prediction_op[1][ind] = val.upper()
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
        prediction_list += predict_next_word(" ".join(pre_list)+pas[1], net_lt, len_n, approximately)
        detra = []
        detro = []
        for x in prediction_list:
            if not x[0] in detra:
                detro.append(x)
                detra.append(x[0])
        prediction_list = detro[0:net_lt]
    for i in range(net_lt - len(prediction_list)):
        prediction_list.append(["", ""])
    # print("pre ".prediction_list)
    return prediction_list


dabile = {}
WORD_LENGTH = 2

with open('a_mod_lit_f_w_tk.txt', "r", encoding="utf-16") as file:
    for line in file:
        line_t = line.split("\t", 2)
        key = line_t[0]
        if len(key.split()) > WORD_LENGTH:
            continue
        value = [line_t[1].split(","), list(map(int, line_t[2].replace("\n", "").split(",")))]
        dabile[key] = value

dabile_key = list(dabile.keys())
dabile_key_df = list(dabile.keys())
for ind, val in enumerate(dabile_key):
    dabile_key[ind] = list(val)



tex = "có thể đó"
print(tex)
print(predict_next_word(tex.lower(), 6, WORD_LENGTH))