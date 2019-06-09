import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib
import matplotlib.pyplot as plt
import json 
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns

plt.rcParams['font.sans-serif']=['SimHei']


movies = pd.read_csv('tmdb_5000_movies.csv',encoding='utf-8')
credits = pd.read_csv('tmdb_5000_credits.csv',encoding='utf-8')#载入数据并读取

json_cols = ['cast','crew']
#json
#编码：把python对象编码转换json字符串   json.dumps
#解码：把json字符串转换成python对象   json.loads
for i in json_cols:
    credits[i] = credits[i].apply(json.loads)
#用json方法汇总所有类型
def get_name(x):
    return ','.join([i['name'] for i in x])

# cast 提取演员

credits['cast'] = credits['cast'].apply(get_name)
# crew 提取导演
def director(x):
    for i in x:
        if i['job'] =='Director':
            return i['name']
credits['crew'] = credits['crew'].apply(director)
print(credits.head())

#将‘crew'转换为’directo‘
credits.rename(columns = {'crew':'director'},inplace=True)
print(credits.head())

#movies 解析
json_colss = ['genres','keywords','spoken_languages','production_countries','production_companies']
for i in json_colss:
    movies[i]=movies[i].apply(json.loads)

def get_names(x):
    return ','.join([i['name'] for i in x])

movies['genres']=movies['genres'].apply(get_names)
movies['keywords']=movies['keywords'].apply(get_names)
movies['spoken_languages']=movies['spoken_languages'].apply(get_names)
movies['production_countries']=movies['production_countries'].apply(get_names)
movies['production_companies']=movies['production_companies'].apply(get_names)

print((credits['title']==movies['title']).describe())

del movies['title']
#合并两张表
df = credits.merge(right=movies,how='inner',left_on='movie_id',right_on='id')
print(df.head())
del df['id']
del df['homepage']
del df['original_title']
del df['tagline']
df['release_date']=df['release_date'].fillna('2014-06-01')#填充缺失值
df['runtime']=df['runtime'].fillna(df.runtime.mean())#填充平均值
df[df[['release_date','runtime']].isnull().values==True]
#获取电影类型
df['genres'][1].split(',')

genre = set()#建立一个集合，会去重
for i in df['genres'].str.split(','):
    genre = set().union(i,genre)

genre = list(genre)
genre.remove('')
print (genre)

#转化日期格式
df['release_year'] = pd.to_datetime(df.release_date, format= '%Y-%m-%d').dt.year
df['release_month'] = pd.to_datetime(df.release_date, format='%Y-%m-%d').dt.month
#判断每部电影属于什么类型，返回1
for genr in genre:
    df[genr] = df['genres'].str.contains(genr).apply(lambda x:1 if x else 0)
        #str.contains 字符串包含

df_gy = df.loc[:,genre]
print(df_gy)

#建立包含电影类型和年份的数据框
print(df_gy.index)
df_gy.index = df['release_year']
print(df_gy.head())
df_gy.groupby('release_year').count().Adventure.plot(figsize=(12,6))
plt.xticks(range(1915,2018,5))
plt.title('电影数量的年度趋势图', fontsize = 20)
plt.xlabel('年份',fontsize = 20)
plt.ylabel('数量',fontsize = 20)
plt.savefig('电影数量的年度趋势图1.png')
plt.show()


df_gy1 = df_gy.sort_index(ascending= False)#sort_index 索引排序，默认升序,False 为降序。
print(df_gy1.head())

df_gys = df_gy1.groupby('release_year').sum()


plt.figure(figsize=(12,6))
plt.plot(df_gys,label = df_gys.columns)#label设置上方小图标签。
plt.legend(df_gys)
plt.xticks(range(1915,2018,5))
plt.title('电影类型随时间的变化',fontsize=20)
plt.xlabel('年份',fontsize = 20)
plt.ylabel('数量',fontsize = 20)
plt.savefig('电影类型随时间的变化2.png')
plt.show()


#计算各类型的电影总数量
df_gysum = df_gys.sum().sort_values(ascending= True)
print(df_gysum)

#电影类型数量条形图
df_gysum.plot.barh(label = 'df_gys', figsize=(15,7))
plt.title('电影类型的数量条形图',fontsize = 20)
plt.xlabel('数量',fontsize=20)
plt.xlabel('电影类型',fontsize=20)
plt.savefig('电影类型3.png')
plt.show()


#各种类型所占比例
b1 = df_gysum/df_gysum.sum()
# #(每一块)之间距离，所占比例大于0.06的，往外高出一点
explode = (b1>=0.06)/20+0.02#设置饼状之间的间距
print(explode)
df_gysum.plot.pie(autopct = '%1.1f%%', figsize = (10,10),label = '',explode = explode)
plt.title('电影类型比例分布图', fontsize = 20)
plt.savefig('电影类型比例分布图4.png')
plt.show()

#电影类型与利润的关系
df['profit'] = df['revenue']-df['budget']
df_gen_pro = pd.DataFrame(index = genre)
#每种类型的平均利润
list =[]
for genr in genre:
    list.append(df.groupby(genr)['profit'].mean())
list2 = []
for i in range(len(genre)):
    list2.append(list[i][1])
df_gen_pro['mean_profit'] = list2
print(df_gen_pro.head())

df_gen_pro.sort_values(by='mean_profit',ascending=True).plot.barh(label='genre',figsize=(15,7))
plt.title('电影类型的利润条形图',fontsize = 20)
plt.xlabel('利润', fontsize=20)
plt.ylabel('电影类型', fontsize=20)
plt.grid(True)
plt.savefig('电影类型的利润条形图5.png')
plt.show()


#电影类型受欢迎条形图
df_gen_popu = pd.DataFrame(index=genre)
list = []
for genr in genre:
    list.append(df.groupby(genr)['popularity'].mean())
list2=[]
for i in range(len(genre)):
    list2.append(list[i][1])
df_gen_popu['mean_popularity']=list2

df_gen_popu.sort_values(by='mean_popularity',ascending=True).plot.barh(label='genre',figsize=(15,7))
plt.title('电影类型受欢迎条形图',fontsize=20)
plt.xlabel('受欢迎',fontsize=20)
plt.ylabel('电影类型',fontsize=20)
plt.grid(True)
plt.savefig('受欢迎电影类型条形图6.png')
plt.show()


#电影预算与票房的关系
plt.scatter(x=df.budget,y=df.revenue)
plt.xlabel('预算',fontsize=20)
plt.ylabel('票房',fontsize=20)
plt.title('电影预算与票房散点图',fontsize=20)
plt.savefig('电影预算与票房的散点图7.png')
plt.show()

#Universal Pictures和Paramount Pictures两个公司产出电影的情况对比
#提取两个公司
df['Universal Pictures']=df['production_companies'].str.contains('Universal Pictures').apply(lambda x:1 if x else 0)
df['Paramount Pictures']=df['production_companies'].str.contains('Paramount Pictures').apply(lambda x:1 if x else 0)
#计算公司利润
df['Universal_profit']=df['Universal Pictures']*df['profit']
df['Paramount_profit']=df['Paramount Pictures']*df['profit']
#计算两个公司的票房
df['Universal_revenue']=df['Universal Pictures']*df['revenue']
df['Paramount_revenue']=df['Paramount Pictures']*df['revenue']

companiesup = [df['Universal Pictures'].sum(),df['Paramount Pictures'].sum()]
print(companiesup)
#比例图
pd.Series(companiesup,index=['Universal Pictures','Paramount Pictures']).plot.pie(autopct='%1.1f%%',figsize=(5,5),label='')
plt.savefig('两公司电影产出对比8.png')
plt.show()


#两家公司的电影随时间变化的趋势对比
companydf = df[['release_year','Universal Pictures','Paramount Pictures','Universal_profit','Paramount_profit','Universal_revenue','Paramount_revenue']]
print(companydf.head())
companydf1 = companydf.sort_index()
print(companydf1.head())
#按年份计算总额
companydf2=companydf1.groupby('release_year').sum()
print(companydf2)
plt.figure(figsize=(12,6))
plt.plot(companydf2.index,companydf2['Universal Pictures'],label=companydf2['Universal Pictures'])
plt.plot(companydf2.index,companydf2['Paramount Pictures'],label=companydf2['Paramount Pictures'])
plt.xticks(range(1915,2018,5))
plt.title('Universal Pictures和Patamount Pictures电影年发行量趋势图对比',fontsize=22)
plt.xlabel('时间',fontsize=15)
plt.ylabel('发行量',fontsize=15)
plt.grid(True)
plt.legend(['Universal Pictures','Patamount Picture'])
plt.savefig('两家公司的电影随时间发行量趋势变化9.png')
plt.show()


#关键词分析
keywords_list = []
for i in df['keywords']:
    keywords_list.append(i)

lst = ''.join(keywords_list)

#制作词云图
wc = WordCloud(background_color='black',max_words=3000,
               scale=1.5).generate(lst)
plt.figure(figsize=(14,7))
plt.imshow(wc)#显示
plt.axis('off')
plt.savefig('词云图.png')
plt.show()

