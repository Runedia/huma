"""
년도별 영화 제작 수

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
from itertools import cycle, islice
from DBMTool import conn
import pandas as pd
from cf import MOVIE_LIST

font_name = font_manager.FontProperties(fname="../assets/D2Coding-Ver1.3.2-20180524.ttf").get_name()
rc('font', family=font_name)


def generate_plot():
    sql = f"""
        SELECT 
            prdtYear, COUNT(*) as '영화 제작 수'
        FROM
            {MOVIE_LIST}
        GROUP BY prdtYear
        ORDER BY prdtYear
    """
    df = pd.read_sql_query(sql, conn)
    print(df)

    my_colors = list(islice(cycle(['#3DADF2', '#69D94A', '#F2D852', '#F2B950', '#F24949']), None, len(df)))
    ax = df.plot(kind='bar', x='prdtYear', y='영화 제작 수', color=my_colors, title='년도별 영화 제작 수')
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

    plt.show()


if __name__ == '__main__':
    generate_plot()
