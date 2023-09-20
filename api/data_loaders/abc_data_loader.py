from abc import ABC, abstractmethod
from typing import Optional

from custom_optional import CustomOptional


class ABCDataLoader(ABC):
    @staticmethod
    @abstractmethod
    def load_json_data(url: str, data_id: Optional[int]) -> CustomOptional:
        pass

    @staticmethod
    @abstractmethod
    def load_image_data(ch_id: int) -> CustomOptional:
        pass
