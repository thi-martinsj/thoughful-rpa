from abc import ABC

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement


class Browser(ABC):
  def _set_webdriver(self) -> webdriver.Chrome:
    raise NotImplementedError

  def goto(self, url: str) -> None:
    raise NotImplementedError

  def close(self) -> None:
    raise NotImplementedError

  def click(self, selector: str) -> None:
    raise NotImplementedError

  def fill(self, selector: str, value: str) -> None:
    raise NotImplementedError

  def wait_to_be_visible(self, selector: str, time: int = 10) -> None:
    raise NotImplementedError

  def select(self, selector: str, value: str) -> None:
    raise NotImplementedError

  def get_element(self, selector: str) -> WebElement:
    raise NotImplementedError

  def get_elements(self, selector: str) -> list[WebElement]:
    raise NotImplementedError

  def get_child_element(self, element: WebElement, selector: str) -> WebElement:
    raise NotImplementedError

  def get_child_elements(self, element: WebElement, selector: str) -> list[WebElement]:
    raise NotImplementedError


class NewsRepository(ABC):
  def fetch_news(self) -> None:
    raise NotImplementedError
