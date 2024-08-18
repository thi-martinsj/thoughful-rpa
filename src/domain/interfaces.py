from abc import ABC


class Browser(ABC):
  def _set_webdriver(self) -> None:
    raise NotImplementedError

  def goto(self, url: str) -> None:
    raise NotImplementedError

  def close(self) -> None:
    raise NotImplementedError
