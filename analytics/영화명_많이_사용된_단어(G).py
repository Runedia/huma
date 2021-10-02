"""
영화명 많이 사용된 단어 (en, ko) G
워드클라우드

최초 작성일: 2021-10-01
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-10-01 | 1.0.0 | 김지호 | 최초작성

<개발 순서>
1. DB 연결
2. 데이터 조회
3. 오류제어
"""

from matplotlib import font_manager, rc, pyplot as plt
from DBMTool import conn
import pandas as pd
from cf import MOVIE_LIST, MOVIE_INFO
from Utils import get_chart_colors

import re
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud

font_path = '../assets/D2Coding-Ver1.3.2-20180524.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def color_func(word, font_size, position, orientation, random_state, **kwargs):
    return f"rgb({random_state.randint(0, 255)},{random_state.randint(0, 255)},{random_state.randint(0, 255)})"


def generated_report():
    sql = f"""
        SELECT 
            ml.movieNm, mi.audits
        FROM
            {MOVIE_LIST} AS ml
                LEFT JOIN
            {MOVIE_INFO} AS mi ON ml.movieCd = mi.movieCd
        WHERE
            mi.audits != ''
                AND mi.audits != '청소년관람불가'
    """
    df = pd.read_sql_query(sql, conn)

    nlp = Okt()
    words = []

    for idx, data in df.iterrows():
        msg = re.sub(r'[^\w]', ' ', data[0])
        words += nlp.phrases(msg)

    count = Counter(words)

    word_count = dict()
    for tag, counts in count.most_common(30):
        if len(str(tag)) > 1:
            word_count[tag] = counts

    plt.figure(figsize=(12, 5))
    plt.xlabel('키워드')
    plt.ylabel('빈도수')
    plt.grid(True)
    sorted_key = sorted(word_count, key=word_count.get, reverse=True)
    sorted_values = sorted(word_count.values(), reverse=True)
    plt.bar(range(len(word_count)), sorted_values, align='center', color=get_chart_colors(df))
    plt.xticks(range(len(word_count)), list(sorted_key), rotation='75')
    plt.title('영화명에 많이 사용된 단어 (G)')
    plt.show()

    word_count = dict()
    for tag, counts in count.most_common(100):
        if len(str(tag)) > 1:
            word_count[tag] = counts

    wc = WordCloud(font_path, background_color='ivory', width=800, height=600, color_func=color_func, random_state=True)
    cloud = wc.generate_from_frequencies(word_count)
    plt.figure(figsize=(10, 10))
    plt.imshow(cloud)
    plt.axis('off')
    plt.title('영화명에 많이 사용된 단어 (G)')
    plt.show()


if __name__ == '__main__':
    generated_report()
