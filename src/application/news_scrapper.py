import pandas as pd

from src.domain.entities import NewsData
from src.domain.interfaces import NewsRepository


class NewsScrapper:
  def __init__(self, repository: NewsRepository) -> None:
    self._repository = repository

  def get_news(self, phrase: str, category: str, months: int) -> list[NewsData]:
    news_data = self._repository.fetch_news(phrase, category, months)
    return list(map(lambda data: NewsData.from_raw_data(data, phrase), news_data))

  def download_images(self, news_data_list: list[NewsData]):

    for news_data in news_data_list:
      if news_data.image_filename:
        self._repository.download_image(news_data.image_url, news_data.image_filename)

  def save_news_to_excel(self, news_list: list[NewsData], filename: str):
    news_data_list = [news.to_dict() for news in news_list]

    df = pd.DataFrame(news_data_list)
    df.to_excel(f"./output/{filename}.xlsx")
