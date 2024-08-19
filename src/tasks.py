from robocorp.tasks import task

from .infrastructure.browsers.chrome_browser import ChromeBrowser
from .infrastructure.repositories.ap_news_repository import APNewsRepository


@task
def minimal_task():
    ap_news_repo = APNewsRepository(ChromeBrowser())
    ap_news_repo.fecth_news("test", "stories", 2)

