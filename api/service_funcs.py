import json
import urllib.request


def load_people_cnt(people_url: str) -> int:
    with urllib.request.urlopen(people_url) as response:
        return json.loads(response.read())["count"]
