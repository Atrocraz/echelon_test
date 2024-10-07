"""test_assets.py.

Модуль, содержащий тесты для проверки корректности работы
страниц списка активов, информации об активе и создания актива.
"""
import datetime as dt
from os import getenv
from typing import Callable

import allure
import pytest
from dotenv import load_dotenv

from .logs_manager import DockerLogs
from .pages.asset_page import AssetPage
from .pages.assets_list_page import AssetsListPage
from .pages.main_page import MainPage


@allure.title("Класс тестов создания актива")
@pytest.mark.assets
class TestCreateAsset:
    """Класс тестов создания актива."""

    @allure.title("Тест страницы актива после создания нового")
    def test_asset_info_page_on_creation(self, browser: Callable,
                                         expected_values: dict) -> None:
        """Тест для проверки корректности отображаемых данных.

        Проверяет корректность данных на странице актива.
        """
        timestamp = dt.datetime.now(tz=dt.timezone.utc)
        logs_manager = DockerLogs()
        load_dotenv()
        project_url = getenv("PROJECT_URL")
        page, asset_id, tag_name, _ = self.create_new_asset_from_assets_page(
            browser)

        with allure.step("Переход на страницу нового актива"):
            page.go_to_asset_page(asset_id)
        page = AssetPage(browser,
                         f"{project_url}app/assets/{asset_id}/info")
        with allure.step("Получение информации о новом активе с его страницы"):
            asset_data = page.get_asset_data()

        with allure.step("Проверка корректности информации об активе"):
            expected_values["Название"] += str(asset_id)
            for name, value in asset_data.items():
                if (name in expected_values and
                        expected_values.get(name) != value):
                    error_message = (
                        f"Некорректное значение в поле '{name}': {value}."
                    )
                    raise AssertionError(error_message)

        with allure.step("Проверка корректности выбранных тэгов актива"):
            self.validate_tags(asset_data, tag_name)

        logs_manager.get_docker_logs(since=timestamp)

    @allure.title("Тест списка активов после создания нового")
    def test_asset_info_in_list_on_creation(self, browser: Callable,
                                            expected_values: dict) -> None:
        """Тест для проверки корректности отображаемых данных.

        Проверяет корректность данных на странице списка активов.
        """
        timestamp = dt.datetime.now(tz=dt.timezone.utc)
        logs_manager = DockerLogs()
        (page, asset_id, tag_name,
         new_asset) = self.create_new_asset_from_assets_page(browser)

        with allure.step("Получение информации об активе в списке"):
            asset_data = page.get_asset_data_in_list(new_asset)

        with allure.step("Проверка корректности информации об активе"):
            expected_values["Название"] += str(asset_id)
            for name, value in asset_data.items():
                if (name in expected_values and
                        expected_values.get(name) != value):
                    error_message = (
                        f"Некорректное значение в поле '{name}': {value}."
                    )
                    raise AssertionError(error_message)

        with allure.step("Проверка корректности выбранных тэгов актива"):
            self.validate_tags(asset_data, tag_name)

        logs_manager.get_docker_logs(since=timestamp)

    def create_new_asset_from_assets_page(self, browser: Callable) -> tuple:
        """Метод класса для создания нового актива.

        Совершает следующую последовательность действий:
            1. Переход на страницу активов.
            2. Получение id последнего отображаемого актива.
            3. Создание нового актива.
            4. Проверка отображения нового актива в списке активов.

        Возвращает кортеж с PageObject списка активов, id последнего
        отображаемого актива + 1, имя тэга и объект элемента названия
        нового актива в списке.
        """
        load_dotenv()
        project_url = getenv("PROJECT_URL")
        page = MainPage(browser, f"{project_url}")
        with allure.step("Переход на страницу активов"):
            page.go_to_assets_page()

        page = AssetsListPage(browser, f"{project_url}app/assets")
        with allure.step("Получение id последнего отображаемого актива"):
            asset_id = page.get_last_asset_id() + 1

        with allure.step("Создание нового актива"):
            tag_name = page.add_asset(asset_id)
            if tag_name is None:
                error_message = "В базе данных нет тэгов."
                raise AssertionError(error_message)

        with allure.step("Проверка отображения нового актива в списке"):
            new_asset = page.check_new_asset_in_list(asset_id)
            if new_asset is None:
                error_message = "Новый актив не появился в списке активов."
                raise AssertionError(error_message)
        return (page, asset_id, tag_name, new_asset)

    @staticmethod
    def validate_tags(asset_data: dict, tag_name: str) -> None:
        """Метод класса для валидации корректности информации о тэгах."""
        if asset_data["tag_list_inner_text"] == "—":
            error_message = "У актива не выбран тэг. Ожидаемое число тэгов - 1"
            raise AssertionError(error_message)

        if asset_data["tags_amount"] != 1:
            error_message = (
                f"Число тэгов ({asset_data["tags_amount"]}) "
                "не соответствует ожидаемому (1)."
            )
            raise AssertionError(error_message)

        if asset_data["tag_name"] != tag_name:
            error_message = (
                f"Некорректный тэг '{asset_data["tag_name"]}.' "
                f"Ожидаемое значение - '{tag_name}'"
            )
            raise AssertionError(error_message)
