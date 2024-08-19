import json

from robocorp.tasks import task

from .application.news_scrapper import NewsScrapper
from .infrastructure.browsers.chrome_browser import ChromeBrowser
from .infrastructure.repositories.ap_news_repository import APNewsRepository


@task
def extract_news_from_apnews_website():
  with open("./devdata/workitem.json", 'r') as file:
    input_data = json.load(file)

  scrapper = NewsScrapper(APNewsRepository(ChromeBrowser()))
  news = scrapper.get_news(input_data.get("search_phrase"), input_data.get("news_category"), input_data.get("months"))
  scrapper.download_images(news)
  scrapper.save_news_to_excel(news, "news_result")
