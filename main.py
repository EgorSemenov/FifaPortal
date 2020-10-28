import pandas as pd
import re
from decimal import Decimal, ROUND_HALF_UP


# def parse_league_field(league_str):
#     l = league_str.split(',')
#     l = [x.lstrip() for x in l]
#     return l

def parse_league_s(l):
    l.update(l.str.split(','))
    s = []
    for i in l.values:
        for index, item in enumerate(i):
            i[index] = item.lstrip()
        i.pop(0)
        s.append(i.pop(1))
    l.update(l.astype(str))
    l.update(l.str.lstrip('[\'').str.rstrip('\']'))
    return s


def add_s_to_df(d, l, name, index):
    d.insert(index, name, l)


def club(l):
    return l[0]


def league(l):
    return l[1]


# def parse_height(height_str):
#     return float(re.findall(r'\((\d+) cm\)', height_str)[0]) / 100

def parse_height_series(h_s):
    h_s.update(int(re.findall(r'\((\d+) cm\)', x)[0]) for x in h_s)


def count_l_foot(s):
    return s.loc[s == 'Left'].count()


def get_filtered(df, fields, filters):
    """
    take 1-d array(n) with fields and matrix(n1) with values for that fields row by row putting into the 1-d array
    give a suitable part of df
    принимает массив полей и матрицу фильтров, где каждая строка матрицы фильтров это возможные значения
    для соответствующего поля
    :param df:
    :param fields: filtering will be by these fields
    :param filters: matrix: in each rows there are possible values for fields
    :return: suitable rows of df
    """
    map = []                                  # реализовал через маску из True False, если это плохо сообщите пожалуйста
    for i in df[fields].iterrows():
        row = []
        for index, j in enumerate(filters):
            row.append(i[1][index] in j)
        map.append(False not in row)
    return df.loc[map]


fifa_data = pd.read_csv('fifa_players_data.csv', engine='c')
# delete useless columns
fifa_data = fifa_data[
    list(filter(lambda x: x not in ['Skillboost', 'Source', 'Sprint Speed', 'Crossing', 'Curve', 'AGILITY',
                                    'Reactions', 'DEFENDING', 'Marking', 'Stand Tackle', 'Sliding Tackle',
                                    'Aggression', 'SHOOTING', 'Positioning', 'DIVING', 'POSITIONING',
                                    'REFLEXES', 'Reflexes', 'GK Diving', 'GK Kicking', 'GK Positioning',
                                    'HANDLING', 'Special Trait', 'Swipe Skill Move', 'Tap Skill Move'],
                fifa_data.columns))]

parse_height_series(fifa_data['Height'])
add_s_to_df(fifa_data, parse_league_s(fifa_data['League']), 'National team', 4)

# какое количество левоногих в каждой лиге
# amount of left-foot players in each league
df_eng_pr_l = get_filtered(fifa_data, ['League'], [['England Premier League']])
print('Процент левшей в Английской Премьер Лиге:', Decimal(count_l_foot(df_eng_pr_l['Foot']) /
                                                           df_eng_pr_l['Foot'].count() * 100).quantize(Decimal('0.01'),
                                                                                                       rounding=
                                                                                                       ROUND_HALF_UP))
# amount of each nationality in each league
print('Процент французов в Английской Премьер Лиге:', Decimal(get_filtered(df_eng_pr_l, ['Nation'],
                                                                           [['France']])['Nation'].count() /
                                                              df_eng_pr_l['Nation'].count() * 100).quantize(
                                                                                                    Decimal('0.01'),
                                                                                                    rounding=
                                                                                                    ROUND_HALF_UP))
