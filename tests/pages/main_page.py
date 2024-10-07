"""main_page.py.

Модуль, содержащий PageObject главной страницы проекта.
"""
from .header_page import PageWithHeaders


class MainPage(PageWithHeaders):
    """Класс PageObject главной страницы проекта."""

    def __init__(self, *args: tuple, **kwargs) -> None:
        """Метод инициализации экземпляра класса."""
        super(__class__, self).__init__(*args, **kwargs)
