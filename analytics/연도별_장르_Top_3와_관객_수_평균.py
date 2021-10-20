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
from analytics.Utils import init
import json

init()


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
    df['audiAcc'] = df['audiAcc'].fillna(0)
    df['audiAcc'] = df['audiAcc'].astype(int)
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

    df_margin = df_margin.sort_values(by=['prdtYear', 'cnt', 'audiAcc'], ascending=[True, False, False])
    print(df_margin.to_string())

    category = []
    temp = []
    repGenreNm = []
    sub_series = {}

    for idx, data in df_prdtyear.iterrows():
        prdtYear = data[1]
        category.append(prdtYear)
        df_temp = df[df['prdtYear'] == prdtYear].head(3).copy()

        for cnt in range(3):
            name = df_temp['repGenreNm'].iloc[cnt]
            repGenreNm.append(name)
            temp.append({
                'year': prdtYear,
                'name': name,
                'auditot': int(df_temp['cnt'].iloc[cnt]),
                'audiavg': int(df_temp['관객 수'].iloc[cnt])
            })
            # 타입 오류로 인해 int로 변환 (Object of type int64 is not JSON serializable)

    repGenreNm = list(dict.fromkeys(repGenreNm))
    series = []

    for item in repGenreNm:
        series.append({
            'name': item,
            'type': 'bar',
            'stack': 'genre',
            'emphasis': {
                'focus': 'series',
            },
            'data': [],
        })

    for idx, data in df_prdtyear.iterrows():
        prdtYear = data[1]
        tempdata = {}
        tempdata_audiavg = {}
        for item in repGenreNm:
            tempdata[item] = 0
            tempdata_audiavg[item] = 0

        for cnt in range(3):
            result = list(filter(lambda x: x['year'] == prdtYear, temp))
            for sdata in result:
                tempdata[sdata['name']] = sdata['auditot']
                tempdata_audiavg[sdata['name']] = sdata['audiavg']

        for gen in repGenreNm:
            pos = next((index for (index, item) in enumerate(series) if item['name'] == gen), None)
            series[pos]['data'].append(tempdata[gen])

        sub_series[prdtYear] = []
        for gen in repGenreNm:
            sub_series[prdtYear].append({
                'name': gen,
                'value': tempdata_audiavg[gen]
            })

    jsonData = {
        'category': category,
        'series': series,
        'sub_series': sub_series,
    }
    print(jsonData)

    with open('./Chart2.json', 'w') as outfile:
        json.dump(jsonData, outfile)

    # ax = df_margin.plot(kind='bar', x='prdtYear', y='영화 수', color=color_chart_func(df_margin), title='연도별 개봉 영화 수')
    plt.figure(figsize=(12, 6))
    ax = df_margin.pivot(index='prdtYear', columns='repGenreNm', values='cnt').plot(kind='bar')
    ax.set_xlabel(None)

    # x 축 label 각도
    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    # plt.show()

    # 차트 모양 고민 필요
    # Vue.js로 만듬.


if __name__ == '__main__':
    generated_report()
