"""locators.py.

Модуль, содержащий классы с константами локаторов.
"""
from selenium.webdriver.common.by import By


class BaseLocators:
    """Класс с локаторами, общими для всех страниц."""

    PARENT_ELEMENT = (By.XPATH, "./..")


class HeaderPageLocators:
    """Класс с локаторами, общими для всех страниц с заголовками."""

    ASSETS_LINK = (By.PARTIAL_LINK_TEXT, "Активы")


class AssetsListPageLocators:
    """Класс с локаторами для страницы списка активов."""

    NEW_ASSET_BUTTON = (By.XPATH, "//*[contains(text(), 'Добавить актив')]")
    ADD_FORM = (By.CLASS_NAME, "asset-new__form")
    ADD_FORM_NAME = (By.NAME, "name")
    ADD_FORM_ADDRESS_TYPE = (By.NAME, "AddressType")
    ADD_FORM_IPv4_TYPE = (By.ID, "IPv4")
    ADD_FORM_ADDRESS = (By.NAME, "Address")
    ADD_FORM_IMPORTANCE_TYPE = (By.NAME, "importanceType")
    ADD_FORM_IMPORTANCE_HIGH = (By.ID, "IMPORTANCE_TYPE_HIGH")
    ADD_FORM_OS_TYPE = (By.NAME, "osType")
    ADD_FORM_OS_MAC = (By.ID, "OPERATING_SYSTEM_TYPE_MACOS")
    ADD_FORM_DEVICE_TYPE = (By.NAME, "deviceType")
    ADD_FORM_DEVICE_TERMINAL = (By.ID, "DEVICE_TYPE_TERMINAL")
    ADD_FORM_OPEN_TAGS_SELECTION = (By.ID, "select-tags")
    ADD_FORM_FIRST_TAG = (By.CLASS_NAME, "checkbox__label-wrapper")
    ADD_FORM_FIRST_TAG_NAME = (By.CLASS_NAME, "checkbox__label")
    ADD_FORM_CREATE_BUTTON = (By.XPATH, "//*[contains(text(), 'Создать')]")
    ASSET_ROW = (By.CLASS_NAME, "MuiDataGrid-row")
    ASSET_IMPORTANCE_TYPE_IN_TABLE = (By.CSS_SELECTOR, ".Jjwgf1Fx.dUrFZNha")
    ASSET_TEXT_VALUES_IN_TABLE = (By.CLASS_NAME, "oeKpKvKw")
    ASSET_TAG_ELEMENT_IN_TABLE = (
        By.CSS_SELECTOR,
        ".sc-eKBdFk.Tfaui.MuiBox-root",
    )
    ASSET_TAG_LIST_IN_TABLE = (By.CLASS_NAME, "assets-table-tags")
    ASSET_TAGS_TAG_IN_TABLE = (By.TAG_NAME, "div")
    ASSET_TAGS_AMOUNT_IN_TABLE = (
        By.CLASS_NAME,
        "assets-table-tags__more-tags",
    )
    ASSET_TAG_NAME_IN_TABLE = (
        By.CSS_SELECTOR,
        ".assets-table-tags__tag.assets-table-tags__tag_dark",
    )


class AssetInfoPageLocators:
    """Класс с локаторами для страницы с информацией об активе."""

    ASSET_ABOUT_LIST = (By.CLASS_NAME, "about-asset-list")
    ASSET_ABOUT_ITEM = (By.CLASS_NAME, "about-asset-list__item")
    ASSET_ABOUT_ITEM_LABEL = (By.CLASS_NAME, "about-asset-list__label")
    ASSET_ABOUT_ITEM_VALUE = (By.CLASS_NAME, "about-asset-list__value")
    ASSET_ABOUT_TAG_LIST = (By.CLASS_NAME, "about-asset-list__tags")
    ASSET_ABOUT_TAGS_TAG = (By.TAG_NAME, "a")
    ASSET_ABOUT_TAG_NAME = (By.CLASS_NAME, "tag__text")


class LoginPageLocators:
    """Класс с локаторами для страницы авторизации."""

    LOGIN_FIELD = (By.NAME, "Login")
    PASSWORD_FIELD = (By.NAME, "Password")
    LOGIN_BUTTON = (By.XPATH, "//*[contains(text(), 'Войти')]")
