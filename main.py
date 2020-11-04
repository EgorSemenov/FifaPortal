import pandas as pd
import re
from decimal import Decimal, ROUND_HALF_UP
from elasticsearch import Elasticsearch
from elasticsearch import helpers


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


def parse_rating_position_s(s):
    r = s.str.findall(r'[0-9]+')
    r.update(r.apply(int_from_one_elem_l))
    s.update(s.str.findall(r'[A-Z]{2,3}'))
    s.update(s.apply(s_from_one_elem_l))
    return r


def s_from_one_elem_l(l):
    l = str(l[0])
    return l


def int_from_one_elem_l(l):
    l = int(l[0])
    return l


def replace_height_s(s):
    s.update(s.apply(height_int))


def height_int(s):
    return int(re.findall(r'\((\d+) cm\)', s)[0])


def replace_foot_s(s):
    s.replace(to_replace={'Left': 'l', 'Right': 'r'}, inplace=True)


def replace_weak_f_s(s):
    s.update(s.apply(weak_int))


def weak_int(s):
    return int(re.findall(r'\((\d)\)', s)[0])


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
    map = []  # реализовал через маску из True False, если это плохо сообщите пожалуйста
    for i in df[fields].iterrows():
        row = []
        for index, j in enumerate(filters):
            row.append(i[1][index] in j)
        map.append(False not in row)
    return df.loc[map]


def __filter_keys__(d, k):
    return {key: d[key] for key in k}


def doc_generator(df):
    print('Exporting rows in es started...')
    df_iter = df.iterrows()
    keys = df.columns.values
    for i, d in df_iter:
        yield {
            "type": "players",
            "_index": "fifaportal",
            "_id": f"{d['ID']}",
            "_source": __filter_keys__(d, keys),
        }
    print('Exporting rows in es finished...')
    # raise StopIteration


def safe_value(field_val):
    return field_val if not pd.isna(field_val) else 0


def rename_c(df, o_c_name, n_c_name):
    df.update(df.rename(columns={o_c_name: n_c_name}, inplace=True))


fifa_data = pd.read_csv('fifa_players_data.csv', engine='c')
# fifa_data = pd.read_csv('test.csv', engine='c')
es_client = Elasticsearch(http_compress=True)

# delete useless columns
fifa_data = fifa_data[
    list(filter(lambda x: x not in ['Skillboost', 'Source', 'Sprint Speed', 'Crossing', 'Curve', 'AGILITY',
                                    'Reactions', 'DEFENDING', 'Marking', 'Stand Tackle', 'Sliding Tackle',
                                    'Aggression', 'SHOOTING', 'Positioning', 'KICKING', 'DIVING', 'POSITIONING',
                                    'REFLEXES', 'Reflexes', 'GK Diving', 'GK Kicking', 'GK Positioning',
                                    'HANDLING', 'Handling', 'Special Trait', 'Swipe Skill Move', 'Tap Skill Move'],
                fifa_data.columns))]

print('Amount of rows was: ', fifa_data['ID'].count())
fifa_data.dropna(inplace=True)
print('Amount of rows now: ', fifa_data['ID'].count())

replace_height_s(fifa_data['Height'])
add_s_to_df(fifa_data, parse_rating_position_s(fifa_data['Position_Rating']), 'Rating', 5)
rename_c(fifa_data, 'Position_Rating', 'Position')
add_s_to_df(fifa_data, parse_league_s(fifa_data['League']), 'National team', 4)
replace_foot_s(fifa_data['Foot'])
replace_weak_f_s(fifa_data['Weak Foot'])
# print(fifa_data.dtypes)

# for i in fifa_data.columns.values:
#     fifa_data[i] = fifa_data[i].apply(safe_value)

# to es
# helpers.bulk(es_client, doc_generator(fifa_data))
# print(es_client.get(index='fifaportal', id=21503589)['_source'])

# какое количество левоногих в каждой лиге

# amount of left-foot players in each league
# df_eng_pr_l = get_filtered(fifa_da иta, ['League'], [['England Premier League']])
# print('Процент левшей в Английской Премьер Лиге:', Decimal(count_l_foot(df_eng_pr_l['Foot']) /
#                                                           df_eng_pr_l['Foot'].count() * 100).quantize(Decimal('0.01'),
#                                                                                                        rounding=
#                                                                                                        ROUND_HALF_UP))
# # amount of each nationality in each league
# print('Процент французов в Английской Премьер Лиге:', Decimal(get_filtered(df_eng_pr_l, ['Nation'],
#                                                                            [['France']])['Nation'].count() /
#                                                               df_eng_pr_l['Nation'].count() * 100).quantize(
#                                                                                                     Decimal('0.01'),
#                                                                                                     rounding=
#                                                                                                     ROUND_HALF_UP))