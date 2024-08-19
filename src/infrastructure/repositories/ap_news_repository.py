from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging

from RPA.HTTP import HTTP

from src.domain.enums import APNewsCategory
from src.domain.interfaces import Browser, NewsRepository

logger = logging.getLogger(__name__)


class APNewsRepository(NewsRepository):
  def __init__(self, browser: Browser) -> None:
    self._browser = browser

  def fetch_news(self, phrase: str, category: str, number_months: int) -> list[dict]:
    logger.info("[APNewsRepository] Fetching news")

    news_data = []
    self._browser.goto("https://apnews.com/")
    self._search_news(phrase)
    self._filter_news_by_category(category)
    self._extract_data_from_news(number_months, news_data)
    self._browser.close()

    logger.info("[APNewsRepository] Fetched news")
    return news_data

  def download_image(self, url: str, filename: str) -> None:
    logger.info(f"[APNewsRepository] Downloading image. URL: '{url}'")

    http = HTTP()
    http.download(url=url, overwrite=True, target_file=f"./output/news_picture/{filename}.jpg")

    logger.info(f"[APNewsRepository] Successfully downloaded image. URL: '{url}'")

  def _search_news(self, phrase: str):
    self._browser.click(".SearchOverlay-search-button")
    self._browser.fill(".SearchOverlay-search-input", phrase)
    self._browser.click(".SearchOverlay-search-submit")

  def _filter_news_by_category(self, category: str):
    category = category.lower()

    self._browser.select(".Select-input", "3")

    self._browser.wait_to_be_visible(".SearchFilter-heading", 5)

    if category == APNewsCategory.LIVE_BLOGS.value:
      self._browser.click("input_value=00000190-0dc5-d7b0-a1fa-dde7ec030000")

    if category == APNewsCategory.PHOTO_GALLERIES.value:
      self._browser.click("input_value=0000018e-775a-d056-adcf-f75a7d350000")

    if category == APNewsCategory.SECTIONS.value:
      self._browser.click("input_value=00000189-9323-dce2-ad8f-bbe74c770000")

    if category == APNewsCategory.STORIES.value:
      self._browser.click("input_value=00000188-f942-d221-a78c-f9570e360000")

    if category == APNewsCategory.SUBSECTIONS.value:
      self._browser.click("input_value=00000189-9323-db0a-a7f9-9b7fb64a0000")

    if category == APNewsCategory.VIDEOS.value:
      self._browser.click("input_value=00000188-d597-dc35-ab8d-d7bf1ce10000")

    self._browser.click(".SearchResultsModule-formButton")

  def _calculate_date_to_be_stopped(self, number_months: int) -> float:
    number_months -= 1

    if number_months < 0:
      number_months = 0

    last_date = datetime.now() - relativedelta(months=number_months)

    return last_date.timestamp()

  def _extract_data_from_news(self, number_months: int, news_data: list[dict]) -> None:
    stop_date = self._calculate_date_to_be_stopped(number_months)

    result = self._browser.get_element(".SearchResultsModule-results")
    items = self._browser.get_child_elements(result, ".PageList-items-item")

    for item in items:
      title = self._browser.get_child_element(item, ".PagePromo-title").text
      description = item.text
      image = self._browser.get_child_element(item, "tag=img")
      date_element = self._browser.get_child_element(item, "tag=bsp-timestamp")

      image_url = None
      if image:
        image_url = image.get_attribute("src")

      date = None
      if date_element:
        news_timestamp = float(date_element.get_attribute("data-timestamp"))

        if (news_timestamp / 1000) < stop_date:
          break

        date = date_element.text

      news_data.append({
        "title": title,
        "description": description,
        "image_url": image_url,
        "date": date
      })
    else:
      div_next = self._browser.get_element(".Pagination-nextPage")
      self._browser.get_child_element(div_next, "tag=a").click()
      self._extract_data_from_news(number_months, news_data)
