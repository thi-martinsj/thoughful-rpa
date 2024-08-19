from robocorp.tasks import task

from .application.news_scrapper import NewsScrapper
from .infrastructure.browsers.chrome_browser import ChromeBrowser
from .infrastructure.repositories.ap_news_repository import APNewsRepository


@task
def minimal_task():
    scrapper = NewsScrapper(APNewsRepository(ChromeBrowser()))
    news = scrapper.get_news("dollars", "stories", 2)
    scrapper.download_images(news)
    scrapper.save_news_to_excel(news, "news_result")
