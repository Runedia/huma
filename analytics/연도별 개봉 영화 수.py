"""
연도별 개봉 영화 수
막대 차트

최초 작성일: 2021-10-01
작성자: 김지호
버전: 1.0.1

변경이력
- 2021-10-01 | 1.0.0 | 김지호 | 최초작성
- 2021-10-03 | 1.0.1 | 김지호 | 코드 정리
"""

import pandas as pd
from matplotlib import pyplot as plt

from DBMTool import conn
from analytics.Utils import init, color_chart_func
from cf import MOVIE_LIST

init()


def generated_report():
    sql = f"""
        SELECT 
            prdtYear, COUNT(*) as 'mvcnt'
        FROM
            {MOVIE_LIST}
        WHERE prdtStatNm = '개봉'
        GROUP BY prdtYear
        ORDER BY prdtYear
    """
    df = pd.read_sql_query(sql, conn)
    print(df)

    ax = df.plot(kind='bar', x='prdtYear', y='mvcnt', color=color_chart_func(df), title='연도별 개봉 영화 수')
    ax.set_xlabel(None)

    # x 축 label 각도
    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    # data labels
    for p in ax.patches:
        txt = str(p.get_height())
        if len(txt) > 3:
            ax.annotate(txt, (p.get_x() - 0.1, p.get_height() * 1.01))
        else:
            ax.annotate(txt, (p.get_x(), p.get_height() * 1.01))

    # plt.show()


if __name__ == '__main__':
    generated_report()
