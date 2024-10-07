"""header_page.py.

Модуль, содержащий базовый PageObject для последующего использования
в качестве родительского класса для PageObject проекта, на которых присутствует
элемент заголовка.
"""
from .base_page import BasePage
from .locators import HeaderPageLocators


class PageWithHeaders(BasePage):
    """Базовый класс PageObject.

    Дополняет класс BasePage методами нажатия на элементы заголовка.
    """

    def go_to_assets_page(self) -> None:
        """Метод для перехода на страницу списка активов."""
        button = self.find_element_with_timeout(HeaderPageLocators.ASSETS_LINK)
        button.click()
