# 情感分析
# -*- coding: utf-8 -*-
# __author__ = 'Su Qianhui'
import text_process as tp
import numpy as np
import pandas as pd

# 1.读取情感词典和待处理文件
# 情感词典
print('reading...')
posdict = tp.read_lines("./emotion_dict/pos_all_dict.txt")
negdict = tp.read_lines("./emotion_dict/neg_all_dict.txt")
# 程度副词词典
mostdict = tp.read_lines('./degree_dict/most.txt')  # 权值为2
verydict = tp.read_lines('./degree_dict/very.txt')  # 权值为1.5
moredict = tp.read_lines('./degree_dict/more.txt')  # 权值为1.25
ishdict = tp.read_lines('./degree_dict/ish.txt')  # 权值为0.5
insufficientdict = tp.read_lines('./degree_dict/insufficiently.txt')  # 权值为0.25
inversedict = tp.read_lines('./degree_dict/inverse.txt')  # 权值为-1

# 情感波动级别
emotion_level6 = "情感波动很小，个人情感是不易改变的、经得起考验的。能够理性的看待周围的人和事。"
emotion_level7 = "情感波动较大，周围的喜悦或者悲伤都能轻易的感染他，他对周围的事物有敏感的认知。"


# 2.程度副词处理，根据程度副词的种类不同乘以不同的权值
def match(word, sentiment_value):
    if word in mostdict:  # 例如：极度、太、极其、惊人地
        sentiment_value *= 2.0
    elif word in verydict:  # 例如：不少、很、尤其、着实
        sentiment_value *= 1.75
    elif word in moredict:  # 例如：更加、还要、愈、较为
        sentiment_value *= 1.5
    elif word in ishdict:  # 例如：略微、稍微、一点、未免
        sentiment_value *= 1.2
    elif word in insufficientdict:  # 例如：不怎么、轻度、丝毫、不大
        sentiment_value *= 0.5
    elif word in inversedict:  # 例如：不是、不要、莫、非、难以
        sentiment_value *= -1
    return sentiment_value


# 3.情感得分的最后处理，防止出现负数
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
def transform_to_positive_num(poscount, negcount):
    pos_count = 0
    neg_count = 0
    if poscount < 0 and negcount >= 0:
        neg_count += negcount - poscount
        pos_count = 0
    elif negcount < 0 and poscount >= 0:
        pos_count = poscount - negcount
        neg_count = 0
    elif poscount < 0 and negcount < 0:
        neg_count = -poscount
        pos_count = -negcount
    else:
        pos_count = poscount
        neg_count = negcount
    return (pos_count, neg_count)


# 求单条评论语句的情感倾向总得分
def single_review_sentiment_score(zhihu_sent):
    single_review_senti_score = []
    cuted_review = tp.cut_sentence(zhihu_sent)  # 句子切分，单独对每个句子进行分析

    for sent in cuted_review:
        seg_sent = tp.segmentation(sent)  # 分词
        seg_sent = tp.del_stopwords(seg_sent)[:]  # 去除停用词
        i = 0  # 记录扫描到的词的位置
        s = 0  # 记录情感词的位置
        poscount = 0  # 记录该分句中的积极情感得分
        negcount = 0  # 记录该分句中的消极情感得分

        for word in seg_sent:  # 逐词分析
            # print word
            if word in posdict:  # 如果是积极情感词
                # print "posword:", word
                poscount += 1  # 积极得分+1
                for w in seg_sent[s:i]:
                    poscount = match(w, poscount)
                # print "poscount:", poscount
                s = i + 1  # 记录情感词的位置变化

            elif word in negdict:  # 如果是消极情感词
                # print "negword:", word
                negcount += 1
                for w in seg_sent[s:i]:
                    negcount = match(w, negcount)
                # print "negcount:", negcount
                s = i + 1

            # 如果是感叹号，表示已经到本句句尾
            elif word == "！".encode('utf-8').decode("utf-8") or word == "!".encode('utf-8').decode('utf-8'):
                for w2 in seg_sent[::-1]:  # 倒序扫描感叹号前的情感词，发现后权值+2，然后退出循环
                    if w2 in posdict:
                        poscount += 2
                        break
                    elif w2 in negdict:
                        negcount -= 2
                        break
            i += 1
        # print "poscount,negcount", poscount, negcount
        single_review_senti_score.append(transform_to_positive_num(poscount, negcount))  # 对得分做最后处理
    pos_result, neg_result = 0, 0  # 分别记录积极情感总得分和消极情感总得分
    for res1, res2 in single_review_senti_score:  # 每个分句循环累加
        pos_result += res1
        neg_result += res2
    # print pos_result, neg_result
    result = pos_result - neg_result  # 该条评论情感的最终得分
    result = round(result, 1)
    return result


# 4.分析text_test.txt中的所有评论，返回一个列表，列表中元素为（分值，评论）元组
def run_score():
    fp_test = open('text/text_test.txt', 'r', encoding='utf-8')  # 待处理数据
    contents = []
    for content in fp_test.readlines():
        content = content.strip()
        content = content.encode("utf-8").decode("utf-8")
        contents.append(content)
    fp_test.close()
    results = []
    for content in contents:
        score = single_review_sentiment_score(content)  # 对每条评论调用函数求得打分
        results.append((score, content))  # 形成（分数，微博）元组
    return results


# 将（分值，句子）元组按行写入结果文件test_result.txt中
def write_results(results):
    fp_result = open('text/test_result.txt', 'w', encoding='utf-8')
    for result in results:
        fp_result.write(str(result[0]))
        fp_result.write(' ')
        fp_result.write(result[1])
        fp_result.write('\n')
    fp_result.close()


pos_text = []  # 存放消极评论
neg_text = []  # 存放积极评论
mid_text = []  # 存放中立评论


# 求取测试文件中的正负极性的评论比，正负极性分值的平均值比，正负分数分别的方差
def handel_result(results):
    # 正极性评论数量，负极性评论数量，中性评论数量，正负极性比值
    pos_number, neg_number, mid_number, number_ratio = 0, 0, 0, 0
    # 正极性平均得分，负极性平均得分， 比值
    pos_mean, neg_mean, mean_ratio = 0, 0, 0
    # 正极性得分方差，负极性得分方差
    pos_variance, neg_variance, var_ratio = 0, 0, 0
    pos_list = []
    neg_list = []
    middle_list = []
    total_list = []
    for result in results:
        total_list.append(result[0])
        if result[0] > 0:
            pos_list.append(result[0])  # 正极性分值列表
            pos_text.append(result[1])
        elif result[0] < 0:
            neg_list.append(result[0])  # 负极性分值列表
            neg_text.append(result[1])
        else:
            middle_list.append(result[0])
            mid_text.append(result[1])
    #################################各种极性微博数量统计
    pos_number = len(pos_list)
    neg_number = len(neg_list)
    mid_number = len(middle_list)
    total_number = pos_number + neg_number + mid_number
    number_ratio = pos_number / neg_number
    pos_number_ratio = round(float(pos_number) / float(total_number), 2)
    neg_number_ratio = round(float(neg_number) / float(total_number), 2)
    mid_number_ratio = round(float(mid_number) / float(total_number), 2)
    text_pos_number = "积极评论条数为 " + str(pos_number) + " 条，占全部评论比例的 " + str(pos_number_ratio * 100) + "%"
    text_neg_number = "消极评论条数为 " + str(neg_number) + " 条，占全部评论比例的 %" + str(neg_number_ratio * 100) + "%"
    text_mid_number = "中性情感评论条数为 " + str(mid_number) + " 条，占全部评论比例的 %" + str(mid_number_ratio * 100) + "%"
    ##################################正负极性平均得分统计
    pos_array = np.array(pos_list)
    neg_array = np.array(neg_list)  # 使用numpy导入，便于计算
    total_array = np.array(total_list)
    pos_mean = pos_array.mean()
    neg_mean = neg_array.mean()
    total_mean = total_array.mean()  # 求单个列表的平均值
    # 正负进行方差计算
    pos_variance = pos_array.var(axis=0)
    neg_variance = neg_array.var(axis=0)
    total_variance = total_array.var(axis=0)
    if total_variance > 10:  # 赋予不同的情感波动级别
        text_total_var = emotion_level7
    else:
        text_total_var = emotion_level6
    # 构成字典返回
    result_dict = {}
    result_dict['pos_number'] = pos_number  # 正向微博数
    result_dict['neg_number'] = neg_number  # 负向微博数
    result_dict['mid_number'] = mid_number  # 中性微博数
    result_dict['number_ratio'] = round(number_ratio, 1)  # 正负微博数之比，保留一位小数四舍五入
    result_dict['pos_mean'] = round(pos_mean, 1)  # 积极情感平均分
    result_dict['neg_mean'] = round(neg_mean, 1)  # 消极情感平均分
    result_dict['total_mean'] = round(total_mean, 1)  # 总的情感平均得分
    result_dict['pos_variance'] = round(pos_variance, 1)  # 积极得分方差
    result_dict['neg_variance'] = round(neg_variance, 1)  # 消极得分方差
    result_dict['total_variance'] = round(total_variance, 1)  # 总的情感得分方差
    # 各种情感评价
    result_dict['text_pos_number'] = text_pos_number
    result_dict['text_neg_number'] = text_neg_number
    result_dict['text_mid_number'] = text_mid_number
    result_dict['text_total_var'] = text_total_var
    with open('text/result.txt', 'w+') as f:
        d = {'text_pos_number': text_pos_number, 'text_neg_number': text_neg_number, 'text_mid_number': text_mid_number,
             '总情感得分方差': total_variance, '情感波动': text_total_var}
        s = str(d)
        f.write(s)
        f.close()

    return result_dict


def printTable():
    column = ['评论']
    pos = pd.DataFrame(columns=column, data=pos_text)
    pos.to_csv('./text/pos.csv')

    neg = pd.DataFrame(columns=column, data=neg_text)
    neg.to_csv('./text/neg.csv')

    mid = pd.DataFrame(columns=column, data=mid_text)
    mid.to_csv('./text/mid.csv')

    print("已生成表格")


if __name__ == '__main__':
    results = run_score()  # 计算每句话的极性得分，返回list，元素是（得分，微博）
    write_results(results)  # 将每条评论的极性得分都写入文件
    result_dict = handel_result(results)  # 计算结果的各种参数，返回字典
    print(result_dict)
    printTable()
