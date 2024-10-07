"""conftest.py.

Модуль для предварительной подготовки данных для автоматических тестов.
Содержит две фикстуры:
    1. Фикстура browser - отвечает за аутентификацию пользователя,
    получение браузера и версии от пользователя, проверку наличия
    необходимого образа и его загрузку в случае отсутствия, а также
    подготовку объекта WebDriver.
    2. Фикстура expected_values - содержит словарь с ожидаемыми названиями
    HTML элементов и их ожидаемыми значениями.
"""
from os import getenv
from typing import Callable

import allure
import pytest
from dotenv import load_dotenv
from selenium import webdriver

from .pages.login_page import LoginPage
from .selenoid.selenoid import SelenoidManager


@pytest.fixture(scope="class")
@allure.title("Подготовка Pytest фикстуры browser.")
@allure.description("Фикстура, отвечающая за инициализацию объекта WebDriver "
                    "и аутентификацию пользователя.")
def browser(pytestconfig: Callable) -> webdriver.Remote:
    """Фикстура для подготовки элемента webdriver."""
    selenoid_manager = SelenoidManager()
    capmanager = pytestconfig.pluginmanager.getplugin("capturemanager")

    capmanager.suspend_global_capture(in_=True)

    with allure.step("Получение от пользователя названия браузера и версии"):
        browser_type, browser_version = (
            selenoid_manager.get_user_browser_input()
        )

    capmanager.resume_global_capture()

    with allure.step("Проверка наличия docker image браузера "
                     "с требуемой версией"):
        selenoid_manager.download_image_if_not_presented(
            browser_type, browser_version,
        )

    options = selenoid_manager.OPTIONS_CLASSES[browser_type]
    with allure.step("Обновление файла browsers.json"):
        updated: bool = selenoid_manager.update_browsers_json(
            browser_type, browser_version,
        )

    if updated:
        with allure.step("Перезапуск контейнеров Selenoid"):
            selenoid_manager.reload_selenoid_containers()

    with allure.step("Изменение аргументов опций WebDriver"):
        options.add_argument("--ignore-ssl-errors=yes")
        options.add_argument("--ignore-certificate-errors")
        options.browser_version = browser_version
    if browser_type == "opera":
        with allure.step("Дополнительное изменение аргументов для браузера "
                         "Opera в связи с несовместимостью с Selenium 4"):
            options.binary_location = "/usr/bin/opera/"
            options.add_experimental_option("w3c", True)
            options.add_argument("allow-elevated-browser")

    with allure.step("Создание WebDriver"):
        driver = webdriver.Remote(
            "http://localhost:4444/wd/hub", options=options)

    load_dotenv()
    project_url = getenv("PROJECT_URL")
    page = LoginPage(driver, project_url)
    with allure.step("Открытие браузера на главной странице"):
        page.open()
    with allure.step("Аутентификация пользователя"):
        page.sign_up_user()

    return driver


@pytest.fixture
@allure.title("Подготовка Pytest фикстуры expected_values.")
@allure.description("Фикстура, отвечающая за ожидаемые параметры актива.")
def expected_values() -> dict:
    """Фикстура для подготовки словаря ожидаемых элементов для тестов."""
    return {
        "Название": "test",
        "Уровень критичности": "Высокий",
        "Тип устройства": "терминал",
        "FQDN": "—",
        "Имя хоста": "—",
        "IPv4": "192.168.0.3",
        "IPv6": "—",
        "MAC": "—",
        "Тип ОС": "MacOS",
        "Полное название ОС": "—",
        "Название ОС": "—",
        "Вендор": "—",
        "Версия ОС": "—",
        "Код версии ОС": "—",
    }
