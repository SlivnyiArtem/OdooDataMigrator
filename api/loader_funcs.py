from http import HTTPStatus

from api.data_loaders.abc_data_loader import ABCDataLoader
from custom_optional import CustomOptional
from settings.environ_handler import env


def load_sw_data(
    data_id: int, loader: ABCDataLoader
) -> (CustomOptional, CustomOptional, CustomOptional):
    ch_data = loader.load_json_data(env("PEOPLE_URL") + data_id, data_id)
    image_data = loader.load_image_data(data_id)
    if ch_data.status == HTTPStatus.OK:
        home_world_url = ch_data.data["homeworld"]
        planet_data = loader.load_json_data(
            home_world_url, int(home_world_url.rsplit("/", 2)[1])
        )
    else:
        planet_data = CustomOptional(HTTPStatus.NO_CONTENT, None, None, None)
    return ch_data, image_data, planet_data
