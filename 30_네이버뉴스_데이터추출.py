import requests
from bs4 import BeautifulSoup
import pymysql
import pandas as pd

# 1. 웹 크롤링 (네이버 뉴스)
url = 'https://finance.naver.com/news/mainnews.naver?date=2024-10-25'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
res = requests.get(url, headers=header)
soup = BeautifulSoup(res.text, 'html.parser')

# 제목 추출
news_titles = soup.select('dd.articleSubject > a')

# 내용 추출
news_contents = soup.select('dd.articleSummary')

# 크롤링한 데이터 저장
news_article = []
for index, (title, content) in enumerate(zip(news_titles, news_contents)):
    title = title.text.strip()
    content = content.text.strip().replace('\t', '').replace('\n', '')
    news_article.append([index + 1, title, content])

# 데이터프레임에 저장
news_df = pd.DataFrame(news_article, columns=["Index", "Title", "Content"])

# 2. MySQL에 연결
config = {
    'user': 'root',  
    'password': '12341234!!', 
    'host': 'localhost', 
    'database': 'my_db'
}

conn = pymysql.connect(**config)
cursor = conn.cursor()

# 3. 테이블 생성 (테이블이 없으면 생성)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS naver_news (
        `index` INT AUTO_INCREMENT PRIMARY KEY,
        `title` VARCHAR(600),
        `content` TEXT
    );
''')

# 4. 크롤링한 데이터를 MySQL에 삽입
for _, row in news_df.iterrows():
    title = row['Title']
    content = row['Content']
    
    # 쿼리문 실행
    cursor.execute('''
        INSERT INTO naver_news (title, content)
        VALUES (%s, %s);
    ''', (title, content))

# 변경사항 커밋
conn.commit()

# 연결 종료
cursor.close()
conn.close()

print('데이터베이스에 저장 완료')

# 5. CSV로 저장
news_df.to_csv('naver_news.csv', index=False, encoding='utf-8-sig')
print('저장 완료')
