from itertools import cycle, islice

from matplotlib import font_manager, rc

font_path = '../assets/D2Coding-Ver1.3.2-20180524.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


def color_chart_func(df):
    """
    차트에 적용할 색 목록을 반환한다.

    Returns:
        list: 차트 색 목록
    """
    return list(islice(cycle(['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc']), None, len(df)))


def color_wc_func(word, font_size, position, orientation, random_state, **kwargs):
    return f"rgb({random_state.randint(0, 255)},{random_state.randint(0, 255)},{random_state.randint(0, 255)})"
