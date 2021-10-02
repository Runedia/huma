from itertools import cycle, islice


def get_chart_colors(df):
    """
    차트에 적용할 색 목록을 반환한다.

    Returns:
        list: 차트 색 목록
    """
    return list(islice(cycle(['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']), None, len(df)))
