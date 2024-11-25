import requests
from bs4 import BeautifulSoup
import csv
import pymysql

url = 'https://finance.naver.com/news/mainnews.naver?date=2024-10-25'
header = {'User-Agent': 'Mozila/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
res = requests.get(url, headers=header)
soup = BeautifulSoup(res.text, 'html.parser')
#print(soup)

#contentarea_left > div.mainNewsList._replaceNewsLink > ul > li:nth-child(20) > dl > dd.articleSubject > a
#news_title= soup.find('meta',{'property':'og:title'})
# title = news_title['content']

#title 추출
#contentarea_left > ul > li.newsList.top > dl > dd:nth-child(2) > a
news_titles = soup.select('dd.articleSubject > a')

#content 추출
#contentarea_left > div.mainNewsList._replaceNewsLink > ul > li:nth-child(1) > dl > dd.articleSummary
news_contents = soup.select('dd.articleSummary')

news_article = []
for index, (title,content) in enumerate(zip(news_titles,news_contents)):
    title = title.text.strip()
    content = content.text.strip().replace('\t','').replace('\n','')
    news_article.append([index+1, title,content])
print(news_article)

import pandas as pd
news_df = pd.DataFrame(news_article, columns=["#","Title","Content"])
news_df.to_csv('Naver_news.csv', index=False, encoding='utf-8-sig')
print('저장 완료')



