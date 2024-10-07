"""asset_page.py.

Модуль, содержащий PageObject информационной страницы актива.
"""
from .header_page import PageWithHeaders
from .locators import AssetInfoPageLocators


class AssetPage(PageWithHeaders):
    """Класс PageObject информационной страницы актива."""

    def get_asset_data(self) -> dict:
        """Метод класса для получения информации об активе."""
        result = {}

        asset_info_list = self.find_elements_with_timeout(
            AssetInfoPageLocators.ASSET_ABOUT_LIST)
        tags_info = asset_info_list.pop()

        for element in asset_info_list:
            asset_info = self.find_elements_with_timeout(
                AssetInfoPageLocators.ASSET_ABOUT_ITEM, element)
            for elem in asset_info:
                name = self.find_element_with_timeout(
                    AssetInfoPageLocators.ASSET_ABOUT_ITEM_LABEL, elem,
                ).get_attribute("innerHTML")
                value = self.find_element_with_timeout(
                    AssetInfoPageLocators.ASSET_ABOUT_ITEM_VALUE, elem,
                ).get_attribute("innerHTML")
                if name == "Уровень критичности":
                    value = value.split(">")[1].split("<")[0]

                result[name] = value

        tag_list_inner_text = self.find_element_with_timeout(
            AssetInfoPageLocators.ASSET_ABOUT_TAG_LIST, tags_info,
        ).get_attribute("innerHTML")

        result["tag_list_inner_text"] = tag_list_inner_text

        if result["tag_list_inner_text"] == "—":
            return result

        hyper_tags_list = self.find_elements_with_timeout(
            AssetInfoPageLocators.ASSET_ABOUT_TAGS_TAG, tags_info)
        result["tags_amount"] = len(hyper_tags_list)

        tag_name = self.find_element_with_timeout(
            AssetInfoPageLocators.ASSET_ABOUT_TAG_NAME, tags_info,
        ).get_attribute("innerHTML")
        result["tag_name"] = tag_name

        return result
