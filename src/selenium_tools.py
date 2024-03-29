from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os

#download_directory is eval_files
#download_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'eval_files')
download_directory = '/app/src/eval_files'
print(f'Download directory: {download_directory}')


def get_webdriver() -> webdriver:
    time.sleep(3)
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")
    options.add_experimental_option('prefs', prefs)
    #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    #driver = webdriver.Remote("http://10.18.225.150:4444/wd/hub", DesiredCapabilities.CHROME) # stack on docker standalone
    driver = webdriver.Remote("http://10.18.225.150:4445/wd/hub", options=webdriver.ChromeOptions()) # stack on docker swarm
    return driver


def scroll_to_bottom(driver: webdriver) -> dict:

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

    return {'msg': 'Scrolled to bottom', 'success': True}


def get_chrome_driver_status(driver):
    try:
        driver.title
        return "Alive"
    except:
        return "Dead"

def main():
    print(f'Download directory: {download_directory}')


if __name__ == '__main__':
    main()
