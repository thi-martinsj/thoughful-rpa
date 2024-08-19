from robocorp.tasks import task

from .application.news_scrapper import NewsScraper
from .infrastructure.browsers.chrome_browser import ChromeBrowser
from .infrastructure.repositories.ap_news_repository import APNewsRepository


@task
def minimal_task():
    scrapper = NewsScraper(APNewsRepository(ChromeBrowser()))
    news = scrapper.get_news("dollars", "stories", 2)
    scrapper.download_images(news)
