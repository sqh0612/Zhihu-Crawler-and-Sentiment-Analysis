# encoding:UTF-8
import jieba
import numpy as np
import matplotlib.pyplot as plt
import imageio
from snownlp import SnowNLP
from wordcloud import WordCloud, ImageColorGenerator
import csv

pos_textlist = []
neg_textlist = []
mid_textlist = []
sentimentslist = []

def readPos():  # 读取数据
    pos_filename = 'text/pos.csv'
    with open(pos_filename,'r',encoding='utf-8',errors='ignore') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            pos_textlist.append(row[1])
    csvfile.close()

def readNeg():
    neg_filename = 'text/neg.csv'
    with open(neg_filename, 'r', encoding='utf-8', errors='ignore') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            neg_textlist.append(row[1])
    csvfile.close()

def readMid():
    mid_filename = 'text/mid.csv'
    with open(mid_filename, 'r', encoding='utf-8', errors='ignore') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            mid_textlist.append(row[1])
    csvfile.close()

def wordtocloud(textlist,state):
    fulltext = ''
    isCN = 1
    back_coloring = imageio.imread("bd.jpg")
    cloud = WordCloud(font_path='./font.ttf',  # 若是有中文的话，这句代码必须添加，不然会出现方框，不出现汉字
                      background_color="white",  # 背景颜色
                      max_words=2000,  # 词云显示的最大词数
                      mask=back_coloring,  # 设置背景图片
                      max_font_size=100,  # 字体最大值
                      random_state=42,
                      width=1000, height=860, margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
                      )
    for li in textlist:
        fulltext += ' '.join(jieba.cut(li, cut_all=False))
    wc = cloud.generate(fulltext)
    # 分词结果
    image_colors = ImageColorGenerator(back_coloring)
    plt.figure("wordc")
    plt.imshow(wc.recolor(color_func=image_colors))
    wc.to_file(state+'.png')


# def snowanalysis(textlist):
#     for li in textlist:
#         s = SnowNLP(li)
#         sentimentslist.append(s.sentiments)
#     fig1 = plt.figure("sentiment")
#     plt.hist(sentimentslist, bins=np.arange(0, 1, 0.02))
#     plt.show()

def runPos():
    readPos()
    wordtocloud(pos_textlist,'Pos')
    # snowanalysis(pos_textlist)
    print('积极词云输出成功')

def runNeg():
    readNeg()
    wordtocloud(neg_textlist,'Neg')
    # snowanalysis(neg_textlist)
    print('消极词云输出成功')

def runMid():
    readMid()
    wordtocloud(mid_textlist,'Mid')
    # snowanalysis(mid_textlist)
    print('中立词云输出成功')

def run():
    runPos()
    runNeg()
    runMid()

if __name__ == '__main__':
    # 运行
    runPos()
    runNeg()
    runMid()