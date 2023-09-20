from custom_optional import CustomOptional
from odoo_updaters.abs_odoo_updater import ABCOdooUpdater
from services import planet_service, contact_service


class SWOdooUpdater(ABCOdooUpdater):
    def update(self, data_piece: (CustomOptional, CustomOptional, CustomOptional)):
        ch_data, image_data, planet_data = data_piece

        planet = planet_service.update_or_create_planet(
            odoo_connector=self.odoo_connector,
            logger=self.logger,
            planet_data_optional=planet_data,
        )
        contact = contact_service.update_or_create_contact(
            odoo_connector=self.odoo_connector,
            ch_data_optional=ch_data,
            logger=self.logger,
            planet=planet,
            image_data_optional=image_data,
        )
