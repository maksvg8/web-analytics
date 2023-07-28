import pandas as pd
from custom_reports.modules.custom_reporting import *



data1 = {
    'start': ['2023-07-21', '2023-07-21', '2023-07-21', '2023-07-21'],
    'end': ['2023-07-22', '2023-07-23', '2023-07-23', '2023-07-24'],
    'categ': ['4_5', '5_4', '6', '321'],
    'url': ['page/4', 'page/5666', 'page/555', 'page/111'],
    'test': [1,2,3,3]
}



# Создание DataFrame 2
data2 = {
    'date': ['2023-07-22', '2023-07-23', '2023-07-24', '2023-07-24'],
    'url': ['http://example.com/page/4', 'http://example.com/page5', 'http://example.com/page6', 'http://example.com/page/6'],
    'test2': [6,7,8,9]
}



df1 = pd.DataFrame(data1)
df1[['categ', 'url']] = df1[['categ', 'url']].astype(object)
df2 = pd.DataFrame(data2)

# print(df1.info())
# print(df2.info())

df1["start"] = pd.to_datetime(df1["start"], format='%Y-%m-%d')
df1["end"] = pd.to_datetime(df1["end"], format='%Y-%m-%d')
df2["date"] = pd.to_datetime(df2["date"], format='%Y-%m-%d')

# mask1 = df1['date'] == df2['date']
# mask1 = df1['categ'].str.contains(df1['url'])
df1 = transform_banners_sheet(df1)

def sum_banners(df1, df2=None):
    df1['test'] = ''
    for index1, row1 in df1.iterrows():
        pr = row1['categ']
        pr = pr.replace('_', '|')
        pat = rf'^.*({pr}).*'
        mask3 = df2['url'].str.contains(pat, regex=True)
        date_range = pd.date_range(start=row1['start'], end=row1['end'], freq='D')
        print(pat)
        # date_range, type(date_range), 
        print(date_range.astype(str))
        
        mask1 = df2["date"].isin(date_range)
        a = df2.loc[(mask3 & mask1), 'test2'].sum()
        print(a)
        
            # for key, value in sourcePatterns.items():
            #     if re.match(rf"{value}", str(row[campaignColumn])):
            #         df.loc[index, sourceColumn] = key
            #         break
            # else:
            #     df.loc[index, sourceColumn] = "Other Sources"
    return df1

pr = df1['categ'].to_list()
pr = '|'.join(pr)
pat = rf'^.*{pr}.*'
print(pat)
sum_banners(df1, df2)

df_t = df2.drop( 'url', axis=1).groupby('date', as_index=False, sort=False).agg('sum')
df_t.insert(1, 'url', 'all')
print(11111111111111111111111111111111111111111)
print(df_t)

df = pd.DataFrame({'A': [[0, 1, 2], '', [], [3, 4]],
                   'B': [1,1,1,1],
                   'C': [['2023-07-21', '2023-07-22', '2023-07-23'], '2023-07-23', '2023-07-23', ['2023-07-23', '2023-07-24']]})
print(2222222222222222222222222222222222222222)

print(df)
df = df.explode(['A','C']).reset_index(drop=True)
print(df)
df["C"] = pd.to_datetime(df["C"], format='%Y-%m-%d')

# df['date_range'] = pd.date_range(start=df['C'], end=df['C'], freq='D').tolist()

print(df)

'^.*_twitter.*'
mask2 = df1['categ'].isin(df1['url'])
mask3 = df1['url'].str.contains(pat, regex=True)
a = df1.loc[mask3, 'test'].sum()


# in str(df2['url'])

# print(df1['categ'])
# print(mask1)
print(mask2)
print(mask3)
# print(mask1, type(mask1), 111, mask2, type(mask2))

# df1['group'] = ''
# df1['group'] = mask2
# df1.loc[mask2, 'group'] = True

# print(df1)