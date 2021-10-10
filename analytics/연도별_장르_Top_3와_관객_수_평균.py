"""
연도별 장르 Top 3와 관객 수 평균
막대 차트

최초 작성일: 2021-10-07
작성자: 김지호
버전: 1.0.0

변경이력
- 2021-10-07 | 1.0.0 | 김지호 | 최초작성
"""

import pandas as pd
from matplotlib import pyplot as plt

from DBMTool import conn
import analytics.Utils


def generated_report():
    sql = f"""
        SELECT ml.prdtYear,
               ml.repGenreNm,
               COUNT(ml.repGenreNm) AS cnt,
               SUM(box.audiAcc) AS audiAcc
        FROM   movielist AS ml
               LEFT JOIN movieinfo AS mi
                      ON ml.movieCd = mi.movieCd
               LEFT JOIN (SELECT movieCd,
                                 MAX(audiAcc) AS audiAcc
                          FROM   boxofficelist
                          WHERE  openDt IS NOT NULL
                          GROUP  BY movieCd) box
                      ON ml.movieCd = box.movieCd
        WHERE  ml.prdtStatNm = '개봉'
               AND mi.audits != ''
               AND mi.audits != '청소년관람불가'
        GROUP  BY ml.repGenreNm,
                  ml.prdtYear
        ORDER  BY ml.prdtYear,
                  cnt DESC 
                  
    """
    df = pd.read_sql_query(sql, conn)
    df['관객 수'] = (df['audiAcc'] / df['cnt'])

    # 값이 없는 경우가 있다..
    df['관객 수'] = df['관객 수'].fillna(0)
    df['관객 수'] = df['관객 수'].astype(int)

    df_prdtyear = df['prdtYear'].copy()
    df_prdtyear = df_prdtyear.drop_duplicates()
    df_prdtyear = df_prdtyear.reset_index()

    df_margin = df[0:0].copy()

    for idx, data in df_prdtyear.iterrows():
        prdtyear = data[1]

        df_temp = df[df['prdtYear'] == prdtyear].head(3)
        df_margin = pd.concat([df_margin, df_temp])

    print(df_margin.to_string())

    # ax = df_margin.plot(kind='bar', x='prdtYear', y='영화 수', color=color_chart_func(df_margin), title='연도별 개봉 영화 수')
    plt.figure(figsize=(12, 6))
    ax = df_margin.pivot(index='prdtYear', columns='repGenreNm', values='cnt').plot(kind='bar')
    ax.set_xlabel(None)

    # x 축 label 각도
    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    plt.show()

    # 차트 모양 고민 필요


if __name__ == '__main__':
    generated_report()
