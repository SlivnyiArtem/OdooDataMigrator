from typing import Optional

from custom_optional import CustomOptional
from http import HTTPStatus
from logging import Logger

from odoo_connectors.basic_odoo_connector import BasicOdooConnector


def get_planet_by_name(odoo_connector, name) -> Optional[int]:
    domain = [("name", "=", name)]

    planet = odoo_connector.db_models.execute_kw(
        odoo_connector.db_name,
        odoo_connector.db_uid,
        odoo_connector.db_password,
        "res.planet",
        "search_read",
        [domain],
        {"limit": 1},
    )

    return planet[0]["id"] if planet else None


def modify_planet_data(planet_data_optional: CustomOptional) -> CustomOptional:
    if planet_data_optional.status == HTTPStatus.OK:
        if planet_data_optional.data["name"] != "unknown":
            planet_data = {
                key: val
                for key, val in planet_data_optional.data.items()
                if (
                    key
                    in (
                        "name",
                        "diameter",
                        "population",
                        "rotation_period",
                        "orbital_period",
                    )
                )
                and (val != "unknown")
            }
            planet_data_optional.data = planet_data
            return planet_data_optional
        else:
            return CustomOptional(
                HTTPStatus.NO_CONTENT, None, None, planet_data_optional.data_id
            )
    return planet_data_optional


def update_or_create_planet(
    odoo_connector: BasicOdooConnector,
    logger: Logger,
    planet_data_optional: CustomOptional,
) -> Optional[int]:
    mod_planet_optional = modify_planet_data(planet_data_optional)
    if mod_planet_optional.status != HTTPStatus.OK:
        if mod_planet_optional.status != HTTPStatus.NO_CONTENT:
            logger.info(
                f"Не удалось выгрузить из swapi данные о планете со следующими данными: "
                f"swapi_id: {planet_data_optional.data_id}    - данных о записи нет"
            )
        return None

    existing_planet = get_planet_by_name(
        odoo_connector, mod_planet_optional.data["name"]
    )
    try:
        if existing_planet is not None:
            odoo_connector.db_models.execute_kw(
                odoo_connector.db_name,
                odoo_connector.db_uid,
                odoo_connector.db_password,
                "res.planet",
                "write",
                [[existing_planet], mod_planet_optional.data],
            )
            logger.info(
                f"Успешно обновлены данные о планете {mod_planet_optional.data['name']} "
                f"(swapi_id: {planet_data_optional.data_id}, odoo_id: {existing_planet}, "
                f"пакет обновленных данных  - {mod_planet_optional.data}"
            )
            planet = existing_planet
        else:
            planet = odoo_connector.db_models.execute_kw(
                odoo_connector.db_name,
                odoo_connector.db_uid,
                odoo_connector.db_password,
                "res.planet",
                "create",
                [mod_planet_optional.data],
            )
            logger.info(
                f"Успешно создана запись о планете {mod_planet_optional.data['name']} "
                f"(swapi_id: {planet_data_optional.data_id}, odoo_id: {planet}, "
                f"занесеенные данные - {mod_planet_optional.data}"
            )

    except Exception as exc:
        planet = None
        logger.error(
            f"При переносе данных о планете (swapi_id: {planet_data_optional.data_id}) "
            f"возникла непредвиденная ошибка: {exc}"
        )
    return planet
