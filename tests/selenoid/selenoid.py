import docker
import json
import os

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chromium.options import ChromiumOptions as OperaOptions


class SelenoidManager():

    SUPPORTED_BROWSERS = {
        'chrome': 'selenoid/chrome:',
        'opera': 'selenoid/opera:',
        'firefox': 'selenoid/firefox:',
        'microsoft edge': 'browsers/edge:',
        'safari': 'browsers/safari:'
    }
    BROWSERS_JSON_NAMES = {
        'chrome': 'chrome',
        'opera': 'opera',
        'firefox': 'firefox',
        'microsoft edge': 'MicrosoftEdge',
        'safari': 'safari'
    }
    OPTIONS_CLASSES = {
        'chrome': ChromeOptions(),
        'opera': OperaOptions(),
        'firefox': FirefoxOptions(),
        'microsoft edge': EdgeOptions(),
        'safari': SafariOptions()
    }

    def __init__(self):
        self.client = docker.from_env()

    def get_user_browser_input(self):
        browser_type = None
        user_input = input(
            '\nВведите модель браузера для тестирования (quit для выхода) \n'
        )
        browser_type = user_input.lower()
        if browser_type == 'quit':
            exit()
        if browser_type not in self.SUPPORTED_BROWSERS:
            raise Exception('Данный браузер не поддерживается Selenoid')

        browser_version = None
        user_input = input(
            '\nВведите версию браузера для тестирования (quit для выхода) \n'
        )
        if user_input == 'quit':
            exit()
        browser_version = user_input

        return browser_type, browser_version

    def download_image_if_not_presented(self, browser_type, browser_version):
        required_image = (
            self.SUPPORTED_BROWSERS[browser_type] + browser_version)

        image_list = self.client.images.list(name=required_image)

        if not len(image_list):
            try:
                self.client.images.pull(required_image)
            except docker.errors.NotFound as e:
                raise docker.errors.NotFound(
                    'Версия браузера не поддерживается Selenoid, либо введена'
                    ' неверно.\nОжидаемый формат: ###.0'
                ) from e

    def reload_selenoid_containers(self):
        self.client.containers.get('selenoid-selenoid-1').stop()
        self.client.containers.get('selenoid-selenoid-ui-1').stop()
        self.client.containers.get('selenoid-selenoid-1').start()
        self.client.containers.get('selenoid-selenoid-ui-1').start()

    def update_browsers_json(self, browser_type, browser_version):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        file_path = cur_path+'\\browsers.json'
        changed = False

        if not os.path.isfile(file_path):
            raise Exception

        with open(file_path, 'r+', encoding='utf-8') as file:
            data_list = json.load(file)
            name = self.BROWSERS_JSON_NAMES[browser_type]
            image = self.SUPPORTED_BROWSERS[browser_type]+browser_version
            if browser_type == 'chrome' or 'microsoft edge':
                path = "/"
            else:
                path = "/wd/hub"

            if name not in data_list:
                data_list[name] = {
                    "default": browser_version,
                    "versions": {
                        browser_version: {
                            "image": image,
                            "port": "4444",
                            "path": path,
                            "tmpfs": {
                                "/tmp": "size=128m"
                            }
                        }
                    }
                }
                changed = True
            elif browser_version not in data_list[name]['versions']:
                data_list[name]['versions'][browser_version] = (
                    {
                        "image": image,
                        "port": "4444",
                        "path": path,
                        "tmpfs": {
                            "/tmp": "size=128m"
                        }
                    }
                )
                changed = True

            file.seek(0)
            json.dump(data_list, file, indent=4)
            file.close()

        return changed
