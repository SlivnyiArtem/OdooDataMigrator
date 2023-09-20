import base64
import json
import urllib.request
from http import HTTPStatus
from typing import Optional

import requests
from api.data_loaders.abc_data_loader import ABCDataLoader
from settings.environ_handler import env
from custom_optional import CustomOptional
from urllib.error import HTTPError


class SWDataLoader(ABCDataLoader):
    @staticmethod
    def load_json_data(url: str, data_id: Optional[int]) -> CustomOptional:
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                return CustomOptional(HTTPStatus.OK, data, None, data_id)
        except HTTPError as exc:
            return CustomOptional(HTTPStatus.NOT_FOUND, None, str(exc), data_id)

    @staticmethod
    def load_image_data(ch_id: int) -> CustomOptional:
        resp = requests.get(env("IMAGE_URL") + str(ch_id) + ".jpg")
        img_data = resp.content
        binary_img = base64.b64encode(img_data).decode()
        if resp.status_code == 200:
            return CustomOptional(HTTPStatus.OK, binary_img, None, ch_id)
        return CustomOptional(HTTPStatus.NOT_FOUND, None, str(FileNotFoundError), ch_id)
