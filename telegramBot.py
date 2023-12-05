import telegram
import asyncio
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


async def send_news():
    bot = telegram.Bot(token='1')
    chat_id = -1
    news_titles = get_news_titles()
    await bot.send_message(chat_id=chat_id, text='최신뉴스입니다.' "\n\n\n\n" + news_titles)

def get_news_titles() -> str:
    url = r"원하는 검색어 링크"
    res = requests.get(url)

    with webdriver.Chrome() as driver:
        driver.get(url)
        time.sleep(2)

        new_news = driver.find_element(By.XPATH, '//*[@id="snb"]/div[1]/div/div[1]/a[2]')
        new_news.click()

        time.sleep(2)
        soup = BeautifulSoup(res.content, 'html.parser')
        news_data = []
        for link in soup.find_all("a", "news_tit"):
            title = link.text
            href = link['href']
            news_data.append(f"{title}\n{href}")

        return "\n\n".join(news_data)

if __name__ == "__main__":
    asyncio.run(send_news())
