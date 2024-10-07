"""login_page.py.

Модуль, содержащий PageObject страницы авторизации.
"""
from .base_page import BasePage
from .locators import LoginPageLocators


class LoginPage(BasePage):
    """Класс PageObject страницы авторизации."""

    def sign_up_user(self) -> None:
        """Метод авторизации пользователя.

        Производит авторизацию с логином и паролем 'admin'
        """
        self.find_element_with_timeout(
            LoginPageLocators.LOGIN_FIELD,
        ).send_keys("admin")
        self.find_element_with_timeout(
            LoginPageLocators.PASSWORD_FIELD,
        ).send_keys("admin")
        self.press_button_when_clickable(LoginPageLocators.LOGIN_BUTTON)
