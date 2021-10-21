"""
관람객 순위 Top 10
막대 차트

최초 작성일: 2021-10-07
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-10-07 | 1.0.0 | 김지호 | 최초작성
"""

import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker

from DBMTool import conn
from analytics.Utils import init, color_chart_func
from cf import BOXOFFICE_LIST

init()


def generated_report():
    sql = f"""
        SELECT 
            *
        FROM
            (SELECT 
                movieCd, movieNm, MAX(audiAcc) AS audiAcc, CAST((MAX(audiAcc) / 10000) AS SIGNED INTEGER) AS "관객 수"
            FROM
                {BOXOFFICE_LIST}
            WHERE
                openDt IS NOT NULL
            GROUP BY movieCd
            ORDER BY movieCd) AS bol
        ORDER BY audiAcc DESC
        LIMIT 10
    """
    df = pd.read_sql_query(sql, conn)
    print(df.to_string())

    # 단위 생성
    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('%d 만명'))

    ax = df.plot(kind='bar', x='movieNm', y='관객 수', color=color_chart_func(df), title='영화별 관람객 순위', ax=ax)
    ax.set_xlabel(None)

    # x 축 label 각도
    for tick in ax.get_xticklabels():
        tick.set_rotation(15)

    # data labels
    for p in ax.patches:
        txt = str(p.get_height())
        ax.annotate(txt, (p.get_x() + 0.1, p.get_height() * 1.01))

    # plt.show()


if __name__ == '__main__':
    generated_report()
