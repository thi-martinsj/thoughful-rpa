import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from src.domain.enums import Selector
from src.domain.interfaces import Browser


class ChromeBrowser(Browser):
  def __init__(self, *args, **kwargs) -> None:
    self._browser_name = "Chrome"
    self._driver = self._set_webdriver()
    self._logger = logging.getLogger(__name__)

  def _set_chrome_options(self) -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=./.user_profile_data")
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-web-security")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-default-apps")
    options.add_argument("--no-first-run")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging", "disable-popup-blocking"])
    options.add_experimental_option("prefs", {'protocol_handler.excluded_schemes.hcp': False})

    return options

  def _set_webdriver(self) -> webdriver.Chrome:
    return webdriver.Chrome(options=self._set_chrome_options())

  def _get_strategy_and_locator(self, selector: str) -> tuple[By, str]:
    if selector.startswith(Selector.CLASS.value):
      return By.CLASS_NAME, selector[1:]

    if selector.startswith(Selector.INPUT_VALUE.value):
      return By.CSS_SELECTOR, f"input[value='{selector[12:]}']"

    if selector.startswith(Selector.TAG.value):
      return By.TAG_NAME, selector[4:]

  def goto(self, url: str) -> None:
    self._logger.info(f"Opening url: {url}")
    self._driver.get(url)

    WebDriverWait(self._driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

  def close(self) -> None:
    self._logger.info("Closing browser")
    self._driver.quit()

  def click(self, selector: str) -> None:
    strategy, locator = self._get_strategy_and_locator(selector)

    self._driver.find_element(strategy, locator).click()

  def fill(self, selector: str, value: str) -> None:
    strategy, locator = self._get_strategy_and_locator(selector)

    WebDriverWait(self._driver, 10).until(
      EC.presence_of_element_located((strategy, locator))
    )

    self._driver.find_element(strategy, locator).send_keys(value)

  def wait_to_be_visible(self, selector: str, time: int = 10) -> None:
    strategy, locator = self._get_strategy_and_locator(selector)

    WebDriverWait(self._driver, time).until(
      EC.presence_of_element_located((strategy, locator))
    )

  def select(self, selector: str, value: str) -> None:
    strategy, locator = self._get_strategy_and_locator(selector)

    element = self._driver.find_element(strategy, locator)
    select = Select(element)
    select.select_by_value(value)

  def get_element(self, selector: str) -> WebElement:
    strategy, locator = self._get_strategy_and_locator(selector)

    return self._driver.find_element(strategy, locator)

  def get_elements(self, selector: str) -> list[WebElement]:
    strategy, locator = self._get_strategy_and_locator(selector)

    return self._driver.find_elements(strategy, locator)

  def get_child_element(self, element: WebElement, selector: str) -> WebElement:
    try:
      strategy, locator = self._get_strategy_and_locator(selector)
      return element.find_element(strategy, locator)
    except Exception:
      return None

  def get_child_elements(self, element: WebElement, selector: str) -> list[WebElement]:
    strategy, locator = self._get_strategy_and_locator(selector)

    return element.find_elements(strategy, locator)
