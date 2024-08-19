import re
from uuid import uuid4


class NewsData:
  def __init__(self) -> None:
    self.title = ""
    self.date = None
    self.description = ""
    self.image_filename = None
    self.image_url = None
    self.count_search_phrase = None
    self.contains_money = False

  @staticmethod
  def from_raw_data(raw_data: dict, phrase: str) -> "NewsData":
    news_data = NewsData()

    news_data.title = raw_data.get("title", "")
    news_data.date = raw_data.get("date")
    news_data.description = raw_data.get("description", "")
    news_data.image_filename = f"{str(uuid4())}.jpg" if raw_data.get("image_url") else None
    news_data.image_url = raw_data.get("image_url")

    news_data.count_search_phrase = news_data.title.lower().count(phrase.lower()) + \
      news_data.description.lower().count(phrase.lower())

    news_data.contains_money = bool(re.search(r"\$\d+(\.\d{1,2})?|USD|\d+\s+dollars", news_data.title)) or \
      bool(re.search(r"\$\d+(\.\d{1,2})?|USD|\d+\s+dollars", news_data.description))

    return news_data
