from http import HTTPStatus
from typing import Optional

from custom_optional import CustomOptional
from logging import Logger

from odoo_connectors.basic_odoo_connector import BasicOdooConnector


def update_or_create_contact(
        odoo_connector: BasicOdooConnector,
        ch_data_optional: CustomOptional,
        logger: Logger,
        planet=None,
        image_data_optional: CustomOptional = None,
) -> Optional[int]:
    if ch_data_optional.status != HTTPStatus.OK:
        logger.info(
            f"Не удалось выгрузить из swapi данные о контакте со следующими данными: "
            f"swapi_id: {ch_data_optional.data_id}    - данных о записи нет"
        )
        return None
    name = ch_data_optional.data["name"]
    values = {
        "name": name,
    }
    if planet is not None:
        values["planet"] = planet
    if image_data_optional.data is not None:
        values["image_1920"] = image_data_optional.data
    else:
        logger.error(
            f"Не удалось выгрузить изображение с идентификатором: {image_data_optional.data_id}"
        )
    try:
        contact_id = get_contact_by_name(odoo_connector, name)
        if contact_id is not None:
            odoo_connector.db_models.execute_kw(
                odoo_connector.db_name,
                odoo_connector.db_uid,
                odoo_connector.db_password,
                "res.partner",
                "write",
                [[contact_id], values],
            )

            logger.info(
                f"Успешно обновлены данные о контакте {values['name']} "
                f"(swapi_id: {ch_data_optional.data_id}, odoo_id: {contact_id}, "
                f"пакет обновленных данных  - {values}"
            )
        else:
            contact_id = odoo_connector.db_models.execute_kw(
                odoo_connector.db_name,
                odoo_connector.db_uid,
                odoo_connector.db_password,
                "res.partner",
                "create",
                [values],
            )

            logger.info(
                f"Успешно создана запись о контакте {values['name']} "
                f"(swapi_id: {ch_data_optional.data_id}, odoo_id: {contact_id})"
            )
    except Exception as exc:
        contact_id = None
        logger.error(
            f"При переносе данных о контакте (swapi_id: {ch_data_optional.data_id})"
            f" возникла непредвиденная ошибка: {exc}"
        )
    return contact_id


def get_contact_by_name(odoo_connector: BasicOdooConnector, name: str) -> Optional[int]:
    domain = [("name", "=", name)]
    contact = odoo_connector.db_models.execute_kw(
        odoo_connector.db_name,
        odoo_connector.db_uid,
        odoo_connector.db_password,
        "res.partner",
        "search_read",
        [domain],
        {"limit": 1},
    )
    return contact[0]["id"] if contact else None
