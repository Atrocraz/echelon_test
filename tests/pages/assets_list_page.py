"""assets_list_page.py.

Модуль, содержащий PageObject страницы списка активов.
"""
from selenium.common import exceptions as exc
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebElement

from .header_page import PageWithHeaders
from .locators import AssetsListPageLocators, BaseLocators


class AssetsListPage(PageWithHeaders):
    """Класс PageObject страницы списка активов."""

    def add_asset(self, last_asset_id: int) -> str:
        """Метод класса для создания нового актива."""
        self.press_button_when_clickable(
            AssetsListPageLocators.NEW_ASSET_BUTTON,
        )

        form = self.find_element_with_timeout(AssetsListPageLocators.ADD_FORM)

        self.find_element_with_timeout(
            AssetsListPageLocators.ADD_FORM_NAME,
        ).send_keys("test"+str(last_asset_id))
        self.select_option_from_list(
            form,
            AssetsListPageLocators.ADD_FORM_ADDRESS_TYPE,
            AssetsListPageLocators.ADD_FORM_IPv4_TYPE,
        )
        self.find_element_with_timeout(
            AssetsListPageLocators.ADD_FORM_ADDRESS,
        ).send_keys("192.168.0.3")
        self.select_option_from_list(
            form,
            AssetsListPageLocators.ADD_FORM_IMPORTANCE_TYPE,
            AssetsListPageLocators.ADD_FORM_IMPORTANCE_HIGH,
        )
        self.select_option_from_list(
            form,
            AssetsListPageLocators.ADD_FORM_OS_TYPE,
            AssetsListPageLocators.ADD_FORM_OS_MAC,
        )
        self.select_option_from_list(
            form,
            AssetsListPageLocators.ADD_FORM_DEVICE_TYPE,
            AssetsListPageLocators.ADD_FORM_DEVICE_TERMINAL,
        )
        self.press_button_when_clickable(
            AssetsListPageLocators.ADD_FORM_OPEN_TAGS_SELECTION)
        try:
            first_tag = self.find_element_with_timeout(
                AssetsListPageLocators.ADD_FORM_FIRST_TAG)
            tag_name: str = self.find_element_with_timeout(
                AssetsListPageLocators.ADD_FORM_FIRST_TAG_NAME,
                first_tag,
            ).get_attribute("innerHTML")
            self.press_button_when_clickable(
                AssetsListPageLocators.ADD_FORM_FIRST_TAG)
        except exc.TimeoutException:
            tag_name = None

        self.press_button_when_clickable(
            AssetsListPageLocators.ADD_FORM_CREATE_BUTTON)

        return tag_name

    def check_new_asset_in_list(self, asset_id: int) -> WebElement:
        """Метод класса для проверки наличия на странице актива.

        Поиск производится по ожидаемому имени актива.
        """
        asset_name = "test" + str(asset_id)
        try:
            return self.find_element_with_timeout(
                (By.XPATH, f"//*[contains(text(), '{asset_name}')]"),
            )
        except exc.TimeoutException:
            return None

    def get_asset_data_in_list(self, name_object: WebElement) -> dict:
        """Метод класса для получения информации об активе из списка."""
        tags_block_order_number = 4
        text_results_order = {
            0: "Название",
            1: "IPv4",
            2: "Тип устройства",
            3: "Тип ОС",
        }
        result = {}

        name_data_row = self.find_element_with_timeout(
            BaseLocators.PARENT_ELEMENT, name_object)
        asset_data_row = self.find_element_with_timeout(
            BaseLocators.PARENT_ELEMENT, name_data_row)

        result["Уровень критичности"] = self.find_element_with_timeout(
            AssetsListPageLocators.ASSET_IMPORTANCE_TYPE_IN_TABLE,
            asset_data_row,
        ).get_attribute("title")

        text_results_elements = self.find_elements_with_timeout(
            AssetsListPageLocators.ASSET_TEXT_VALUES_IN_TABLE,
            asset_data_row,
        )

        for i, element in enumerate(text_results_elements):
            if i == tags_block_order_number:
                break

            result[text_results_order[i]] = element.get_attribute("innerHTML")

        result["tag_list_inner_text"] = self.find_element_with_timeout(
            AssetsListPageLocators.ASSET_TAG_ELEMENT_IN_TABLE,
            asset_data_row,
        ).get_attribute("innerHTML")

        if result["tag_list_inner_text"] == "—":
            return result

        tags_list_element = self.find_element_with_timeout(
            AssetsListPageLocators.ASSET_TAG_LIST_IN_TABLE,
            asset_data_row,
        )
        tags_elements = self.find_elements_with_timeout(
            AssetsListPageLocators.ASSET_TAGS_TAG_IN_TABLE,
            tags_list_element,
        )

        tags_amount = 1
        if len(tags_elements) > 1:
            tags_amount += self.find_element_with_timeout(
                AssetsListPageLocators.ASSET_TAGS_AMOUNT_IN_TABLE,
                tags_list_element,
            ).get_attribute("innerHTML")
        result["tags_amount"] = tags_amount

        result["tag_name"] = self.find_element_with_timeout(
                AssetsListPageLocators.ASSET_TAG_NAME_IN_TABLE,
                tags_list_element,
            ).get_attribute("innerHTML")

        return result

    def get_last_asset_id(self) -> int:
        """Метод класса для получения айди последнего актива в списке."""
        try:
            last_row = self.find_element_with_timeout(
                AssetsListPageLocators.ASSET_ROW).get_attribute("data-id")
            return int(last_row)
        except exc.TimeoutException:
            return 0

    def go_to_asset_page(self, asset_id: int) -> None:
        """Метод класса для перехода на страницу актива.

        Поиск производится по ожидаемому имени актива.
        """
        asset_name = "test" + str(asset_id)
        self.press_button_when_clickable(
            (By.XPATH, f"//*[contains(text(), '{asset_name}')]"),
        )

    def select_option_from_list(self, scope: WebElement, list_loc: tuple,
                                option_loc: tuple) -> None:
        """Метод класса для выбора элемента в выпадающем списке.

        Производит нажатие на wrapper-элемент нужного значения.
        """
        select = self.find_element_with_timeout(list_loc, scope)
        self.find_element_with_timeout(
            BaseLocators.PARENT_ELEMENT, select).click()
        self.press_button_when_clickable(option_loc)
