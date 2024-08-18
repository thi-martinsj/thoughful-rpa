from robocorp.tasks import task

from .infrastructure.chrome_browser import ChromeBrowser


@task
def minimal_task():
    message = "Hello"
    message = message + " World!"
    browser = ChromeBrowser()
    browser.goto("htpps://www.google.com.br")
