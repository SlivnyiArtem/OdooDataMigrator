from abc import ABC, abstractmethod
from logging import Logger

from custom_optional import CustomOptional
from odoo_connectors.basic_odoo_connector import BasicOdooConnector


class ABCOdooUpdater(ABC):
    def __init__(self, odoo_connector: BasicOdooConnector, logger: Logger):
        self.odoo_connector = odoo_connector
        self.logger = logger

    @abstractmethod
    def update(self, data_piece: (CustomOptional, CustomOptional, CustomOptional)):
        pass
