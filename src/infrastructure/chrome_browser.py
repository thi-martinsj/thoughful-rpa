import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

  def goto(self, url: str) -> None:
    self._logger.info(f"Opening url: {url}")
    self._driver.get(url)

    WebDriverWait(self._driver, 10).until(
      EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

  def close(self) -> None:
    self._logger.info("Closing browser")
    self._driver.quit()
