"""base_page.py.

Модуль, содержащий базовый PageObject для последующего использования
в качестве родительского класса для остальных PageObject проекта.
"""
from selenium.webdriver import Remote
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Базовый класс PageObject.

    Содержит в себе общие для всех дочерних элементов аттрибуты и
    методы.
    """

    BASE_TIMEOUT = 5

    def __init__(self, driver: Remote, url: str) -> None:
        """Метод инициализации экземпляра класса."""
        self.driver = driver
        self.url = url

    def open(self) -> None:
        """Метод для перехода на страницу класса."""
        self.driver.get(self.url)

    def find_element_with_timeout(self, locator: tuple,
                                  scope: WebElement = None,
                                  timeout: int = BASE_TIMEOUT) -> WebElement:
        """Метод класса для поиска элемента на странице с требуемым Timeout."""
        if not scope:
            scope = self.driver

        return WebDriverWait(scope, timeout).until(
            EC.presence_of_element_located(locator),
        )

    def find_elements_with_timeout(self, locator: tuple,
                                   scope: WebElement = None,
                                   timeout: int = BASE_TIMEOUT) -> WebElement:
        """Метод класса для поиска списка элементов.

        Служит для поиска всех подходящих элементов на странице с
        требуемым Timeout.
        """
        if not scope:
            scope = self.driver

        return WebDriverWait(scope, timeout).until(
            EC.presence_of_all_elements_located(locator),
        )

    def press_button_when_clickable(self, locator: tuple,
                                    scope: WebElement = None,
                                    timeout: int = BASE_TIMEOUT) -> WebElement:
        """Метод класса для нажатия на элемент с требуемым Timeout.

        Производит имитацию нажатия на элемент, как только он становится
        доступным для нажатия.
        """
        if not scope:
            scope = self.driver

        WebDriverWait(scope, timeout).until(
            EC.element_to_be_clickable(locator),
        ).click()
