from bs4 import BeautifulSoup
from selenium import webdriver
import tweepy
from datetime import datetime
from datetime import date
import os

def gettoday():

    today = date.today()
    format_today = today.strftime("%Y.%m.%d")
    return format_today

def extract_banner():
    browser = webdriver.Chrome()
    base_url = "http://ticket.yes24.com/New/Notice/NoticeMain.aspx"

    browser.get(base_url)
    soup = BeautifulSoup(browser.page_source, "html.parser")

    results = []
    #슬라이드 배너들
    wrapper = soup.find('div', class_="notice-slide")
    slides = wrapper.find_all('div', class_="swiper-slide")
    #print(slides)
    for slide in slides:
        anchor = slide.find('a')
        link = anchor['href']
        #ticket = anchor.find('div', class_="ticket-txt")
        p1 = anchor.find('p', class_="ticket-date")
        p2 = anchor.find('p', class_="ticket-tit")
        info = {
            'link': link,
            'date': p1.string,
            'title': p2.string
        }
        results.append(info)

    return results

def api():
    auth = tweepy.OAuthHandler(os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET"))
    auth.set_access_token(os.environ.get("TWITTER_ACCESS_TOKEN_KEY"), os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"))

    return tweepy.API(auth)

def tweet(api: tweepy.API, message: str, image_path=None):
    if image_path:
        api.update_status_with_media(message, image_path)
    else:
        api.update_status(message)
    print('Tweeted successfully!')

if __name__ == '__main__':
    api = api()
    #tweet(api, f"http://birthday-color.cafein.jp/html/{date}.html")
    #extract_opening()

    base_url = "http://ticket.yes24.com/New/Notice/NoticeMain.aspx"
    todayis = gettoday()



    results = extract_banner()
    if results == None:
        tweet(api, "no banners!")
    else:
        for result in results:
            full_link = base_url + result['link']
            tweet(api, f"today is {todayis}.\n{full_link}\n{result['date']}\n{result['title']}")

    #extract_opening()
