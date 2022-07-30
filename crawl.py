# 获取知乎评论数据，得到text_test.txt
# -*- coding: utf-8 -*-
# __author__ = 'Su Qianhui'

import requests
from bs4 import BeautifulSoup
import json
import re

textlist = []  #获取的评论列表


def extract_answer(s):
    REG = re.compile('<[^>]*>')
    temp_list = REG.sub("", s).replace("\n", "").replace(" ", "")
    return temp_list

# 评论爬取
def crawl():
    headers = {
        'accept-language': 'zh-CN,zh;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    # 双减政策： 7月24日刚公布--474681128 9月1日新学期开学--483979961 一个月后--488464188
    mid = input("请输入爬取的网页ID：")
    start_url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset=0&sort_by=default'.format(
        mid)
    print("running.")
    next_url = [start_url]
    count = 0

    for url in next_url:
        html = requests.get(url, headers=headers)
        html.encoding = html.apparent_encoding
        soup = BeautifulSoup(html.text, "lxml")
        content = str(soup.p).split("<p>")[1].split("</p>")[0]
        c = json.loads(content)

        if "data" not in c:
            print("获取数据失败，本 ip 可能已被限制。")
            print(c)
            break

        answers = [extract_answer(item["content"]) for item in c["data"] if extract_answer(item["content"]) != ""]

        for answer in answers:
            textlist.append(answer)
            count = count + 1
            # print("answer", count, ":", answer)

        next_url.append(c["paging"]["next"])
        if c["paging"]["is_end"]:
            break

    print("total answers:", count)
    print('评论爬取成功！')

def write_text(textlist):
    fp_result = open('text/text_test.txt', 'w', encoding='utf-8')
    for text in textlist:
        fp_result.write(text)
        fp_result.write('\n')
    fp_result.close()


if __name__ == '__main__':
    # 运行
    crawl()
    write_text(textlist)
