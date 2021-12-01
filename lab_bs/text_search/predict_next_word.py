import json
import underthesea

list_text = []


with open('words.txt', encoding="UTF-8", errors='ignore') as file:
    for line in file:
        json_data = json.loads(line)
        list_text.append(json_data['text'])
print("sta")

PREDICTED_LENGTH = 5


# def Next_Word_Prediction(text, n=3):
#     prediction_list = []
#     text_n = text.split()[-PREDICTED_LENGTH:]
#     while len(text_n) > 0:
#         text = " ".join(text_n)
#         for text_p in list_text:
#             if text == text_p:
#                 continue
#             elif text in text_p:
#                 if text_p.startswith(text):
#                     prediction = text_p.replace(text, "", 1).strip()
#                     prediction_op = [text_p, prediction]
#                     prediction_list.append(prediction_op)
#         prediction_list.sort(key=lambda s: len(s[0]))
#         len_prediction_list = len(prediction_list) >= n
#         for x in prediction_list:
#             if len(x[0].split()) >= PREDICTED_LENGTH and len_prediction_list >= n:
#                 prediction_list.remove(x)
#         if len(prediction_list) >= n:
#             return prediction_list[0:n]
#         text_n.pop(0)
#     if len(prediction_list) > 0:
#         return prediction_list
#     else:
#         return None

def Next_Word_Prediction(text, n=3):
    prediction_list = []
    if text == "":
        for i in range(n):
            prediction_list.append(["", ""])
        return prediction_list
    if text[-1] == " ":
        text_n = text.split()[-PREDICTED_LENGTH:]
        text_n[-1] = text_n[-1]+" "
    else:
        text_n = text.split()[-PREDICTED_LENGTH:]
    while len(text_n) > 0:
        text = " ".join(text_n)
        for text_p in list_text:
            if text == text_p:
                continue
            elif text in text_p:
                if text_p.startswith(text):
                    prediction = text_p.replace(text, "", 1).strip()
                    prediction_op = [text_p, prediction]
                    prediction_list.append(prediction_op)
        prediction_list.sort(key=lambda s: len(s[0]))
        len_prediction_list = len(prediction_list) >= n
        for x in prediction_list:
            if len(x[0].split()) >= PREDICTED_LENGTH and len_prediction_list >= n:
                prediction_list.remove(x)
        if len(prediction_list) >= n:
            return prediction_list[0:n]
        text_n.pop(0)
    for i in range(n-len(prediction_list)):
        prediction_list.append(["", ""])
    return prediction_list


def from_text_Next_Word_Prediction(text, n=3):
    list_text_pd = underthesea.word_tokenize(text)[:-1]
    prediction_list = []
    if text == "":
        for i in range(n):
            prediction_list.append(["", ""])
        return prediction_list
    if text[-1] == " ":
        text_n = text[-PREDICTED_LENGTH*9:].split()[-PREDICTED_LENGTH:]
        text_n[-1] = text_n[-1]+" "
    else:
        text_n = text[-PREDICTED_LENGTH*9:].split()[-PREDICTED_LENGTH:]
    print(text)
    print(text_n)
    len_list_text_pd = len(list_text_pd)
    while len(text_n) > 0:
        text = " ".join(text_n)
        for ind, text_p in enumerate(list_text_pd):
            if text.strip() == text_p:
                if ind < len_list_text_pd:
                    prediction = list_text_pd[ind+1]
                    if text[-1] == " ":
                        prediction_op = [prediction, prediction]
                    else:
                        prediction_op = [prediction, " "+prediction]
                    prediction_list.append(prediction_op)
            elif text in text_p:
                if text_p.startswith(text):
                    prediction = text_p.replace(text, "", 1)
                    prediction_op = [text_p, prediction]
                    prediction_list.append(prediction_op)
        prediction_list.sort(key=lambda s: len(s[0]))
        len_prediction_list = len(prediction_list) >= n
        for x in prediction_list:
            if len(x[0].split()) >= PREDICTED_LENGTH and len_prediction_list >= n:
                prediction_list.remove(x)
        if len(prediction_list) >= n:
            return prediction_list[0:n]
        text_n.pop(0)
    for i in range(n-len(prediction_list)):
        prediction_list.append(["", ""])
    return prediction_list


print(from_text_Next_Word_Prediction("trông tôi khá ốm vì tôi", 10))
# while True:
#     value = input("nhập 1 vài từ: ")
#     STA_Next_Word_Prediction = Next_Word_Prediction(text=value, n=5)
#     for x in STA_Next_Word_Prediction:
#         print(x)
#     value2 = input("ghép với: ")
#     if value2 != "":
#         print(value.strip()+" "+STA_Next_Word_Prediction[int(value2)-1][1])

