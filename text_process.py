# 文本处理
# -*- coding: utf-8 -*-
# __author__ = 'Su Qianhui'

import jieba

print('加载词典...')
import importlib, sys

importlib.reload(sys)


# 分词，返回List
def segmentation(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    return seg_result


# # 分词，词性标注，词和词性构成一个元组
# def postagger(sentence):
#     pos_data = pseg.cut(sentence)
#     pos_list = []
#     for w in pos_data:
#         pos_list.append((w.word, w.flag))
#     return pos_list


# 句子切分
def cut_sentence(words):
    words = words.encode('utf-8').decode('utf8')
    start = 0
    i = 0
    token = 'meaningless'
    sents = []
    punt_list = ',.!?;~，。！？；～… '.encode('utf-8').decode('utf8')
    for word in words:
        if word not in punt_list:  # 如果不是标点符号
            i += 1
            token = list(words[start:i + 2]).pop()
        elif word in punt_list and token in punt_list:  # 处理省略号
            i += 1
            token = list(words[start:i + 2]).pop()
        else:
            sents.append(words[start:i + 1])  # 断句
            start = i + 1
            i += 1
    if start < len(words):  # 处理最后的部分
        sents.append(words[start:])
    return sents


def read_lines(filename):
    fp = open(filename, 'r', encoding='utf-8')
    lines = []
    for line in fp.readlines():
        line = line.strip()
        line = line.encode("utf-8").decode("utf-8")
        lines.append(line)
    fp.close()
    return lines


# 去除停用词
def del_stopwords(seg_sent):
    stopwords = read_lines("./emotion_dict/stop_words.txt")  # 读取停用词表
    new_sent = []  # 去除停用词后的句子
    for word in seg_sent:
        if word in stopwords:
            continue
        else:
            new_sent.append(word)
    return new_sent
